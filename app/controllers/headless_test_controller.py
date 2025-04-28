# app/controllers/headless_test_controller.py
from flask import Blueprint, request, jsonify, current_app
from playwright.sync_api import sync_playwright
from models import Scenario, db  # Import db for committing status updates
from controllers.sse_progress_controller import progress_store  # Import the progress store
import threading
from config import config  # Import the concurrency limit

headless_test_bp = Blueprint('headless_test_bp', __name__)

# Semaphore to limit concurrent headless test threads
test_semaphore = threading.Semaphore(config.MAX_CONCURRENT_TESTS)

def run_headless_tests(payload_id, session_id, app):
    """
    Runs all scenarios in a background thread and updates progress_store for SSE.
    Limits concurrent executions using a semaphore.
    Uses the passed-in app object for app context.
    Creates a new page for each scenario to isolate issues.
    Provides detailed network and console logging for debugging.
    Robustly waits for XSS report network requests with improved logging.
    Ensures page is fully loaded before proceeding with tests.
    """
    with app.app_context():
        with test_semaphore:
            scenarios = Scenario.query.all()
            visited = []
            
            # Initialize progress
            progress_store[session_id] = {"total": len(scenarios), "done": 0}

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)

                for s in scenarios:
                    # Create a new page for each scenario to isolate issues
                    page = browser.new_page()
                    url = f"http://xsslab_app:9090/scenario/{s.id}?payload_id={payload_id}"
                    print(f"\n[+] Visiting: {url}")
                    
                    # Log all network responses
                    def log_response(response):
                        print(f"[Network] {response.status} {response.url}")
                    
                    page.on("response", log_response)
                    
                    # Log all console messages
                    def log_console(msg):
                        print(f"[Console] {msg.type}: {msg.text}")
                    
                    page.on("console", log_console)
                    
                    # Define the endpoints to watch for
                    triggered_url = f"/results/report?scenario_id={s.id}&payload_id={payload_id}"
                    not_triggered_url = "/results/report_not_triggered"

                    def is_report_response(response):
                        # Log all responses for debugging
                        print(f"[Check] Response URL: {response.url}")
                        return (
                            triggered_url in response.url or
                            not_triggered_url in response.url
                        )

                    try:
                        print(f"[Wait] Waiting for XSS report for scenario {s.id} (timeout 2500ms)...")
                        with page.expect_response(is_report_response, timeout=2500):
                            page.goto(url, wait_until="domcontentloaded")
                        s.status = "tested"
                        print(f"[Result] Scenario {s.id} completed.")
                    except Exception:
                        print(f"[Timeout] Scenario {s.id} timed out or did not report.")
                        s.status = "timeout"

                    visited.append({
                        "scenario_id": s.id,
                        "scenario_name": s.name,
                        "url": url
                    })
                    
                    # Update scenario status in DB for progress tracking
                    db.session.commit()
                    
                    # Update progress for SSE
                    progress_store[session_id]["done"] += 1
                    
                    # Close the page to free resources
                    page.close()

                browser.close()
        except Exception as e:
            # Mark any remaining scenarios as error if a global failure occurs
            progress_store[session_id]["done"] = progress_store[session_id]["total"]
            print(f"[Error] Error in headless test thread: {e}")

@headless_test_bp.route('/run_all', methods=['GET'])
def run_all_headless():
    """
    Lance les 20 scénarios XSS via navigateur headless Playwright en arrière-plan.
    Requiert que Playwright soit installé + configuré.
    Le progrès est suivi via SSE en utilisant session_id.
    Limite le nombre de tests concurrents via un sémaphore.
    Uses the application factory pattern.
    Optimized to use wait_for_response instead of static timeouts.
    Enhanced with detailed network and console logging for debugging.
    Creates a new page per scenario to isolate issues.
    """
    payload_id = request.args.get('payload_id', type=int)
    session_id = request.args.get('session_id', type=str)
    if not payload_id or not session_id:
        return jsonify({"error": "Missing ?payload_id=X&session_id=Y"}), 400

    # Get the actual app object and pass it to the thread
    app = current_app._get_current_object()
    thread = threading.Thread(target=run_headless_tests, args=(payload_id, session_id, app))
    thread.daemon = True  # Make thread exit when main thread exits
    thread.start()

    return jsonify({
        "status": "started",
        "payload_id": payload_id,
        "session_id": session_id,
        "note": f"Tests are running in the background (max {config.MAX_CONCURRENT_TESTS} concurrent). Use SSE to track progress."
    })
