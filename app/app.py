import time
from sqlalchemy.exc import OperationalError

from flask import Flask, render_template
from config import config
from db import init_db
from models import db, Scenario
from scenarios.basic_scenarios import basic_scenarios

MAX_DB_RETRIES = 15
RETRY_DELAY = 2  # seconds

# Import des blueprints
from controllers.scenarios_controller import scenarios_bp
from controllers.payloads_controller import payloads_bp
from controllers.results_controller import results_bp
from controllers.auto_test_controller import auto_test_bp
from controllers.headless_test_controller import headless_test_bp





def create_app():
    app = Flask(__name__)
    
    # Retry logic for DB initialization
    for attempt in range(1, MAX_DB_RETRIES + 1):
        try:
            init_db(app)
            break
        except OperationalError as e:
            print(f"[DB INIT] Attempt {attempt}/{MAX_DB_RETRIES} failed: {e}")
            if attempt == MAX_DB_RETRIES:
                print("[DB INIT] Max retries reached. Exiting.")
                raise
            time.sleep(RETRY_DELAY)

    app.config["SERVER_NAME"] = "xsslab_app:9090"

    # Enregistrer les blueprints
    app.register_blueprint(scenarios_bp)
    app.register_blueprint(payloads_bp, url_prefix='/payloads')
    app.register_blueprint(results_bp, url_prefix='/results')
    app.register_blueprint(auto_test_bp, url_prefix='/auto')
    app.register_blueprint(headless_test_bp, url_prefix='/auto_headless')


    # Au démarrage, on s'assure que les scénarios de base existent en DB
    with app.app_context():
        for s in basic_scenarios:
            existing = Scenario.query.filter_by(name=s["name"]).first()
            if not existing:
                new_s = Scenario(name=s["name"], description=s["description"])
                db.session.add(new_s)
        db.session.commit()

    @app.route('/')
    def index():
        last_scenario = Scenario.query.order_by(Scenario.id.desc()).first()
        return render_template('index.html', last_scenario=last_scenario)

    return app

if __name__ == '__main__':
    # Lancer en debug ou en prod
    app = create_app()
    app.run(host='0.0.0.0', port=9090, debug=True, use_reloader=True)
