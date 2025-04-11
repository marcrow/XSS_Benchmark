# app/controllers/headless_test_controller.py
from flask import Blueprint, request, jsonify
from playwright.sync_api import sync_playwright
from models import Scenario

headless_test_bp = Blueprint('headless_test_bp', __name__)

@headless_test_bp.route('/run_all', methods=['GET'])
def run_all_headless():
    """
    Lance les 20 scénarios XSS via navigateur headless Playwright.
    Requiert que Playwright soit installé + configuré.
    """
    payload_id = request.args.get('payload_id', type=int)
    if not payload_id:
        return jsonify({"error": "Missing ?payload_id=X"}), 400

    # Récupération de tous les scénarios
    scenarios = Scenario.query.all()
    visited = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for s in scenarios:
                url = f"http://xsslab_app:9090/scenario/{s.id}?payload_id={payload_id}"
                print(f"[+] Visiting: {url}")
                page.goto(url)
                page.wait_for_timeout(1500)  # attendre exécution JS

                visited.append({
                    "scenario_id": s.id,
                    "scenario_name": s.name,
                    "url": url
                })

            browser.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "status": "completed",
        "payload_id": payload_id,
        "tested": visited,
        "note": "Les XSS doivent être reportées via notifyXSS()"
    })
