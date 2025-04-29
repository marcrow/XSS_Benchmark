import time
from sqlalchemy.exc import OperationalError
from sqlalchemy import text  # Import text for SQLAlchemy 2.x

from flask import Flask, render_template
from config import config
from db import db  # Import the single SQLAlchemy instance
from models import Scenario, Payload
from scenarios.sync import sync_scenarios_to_db

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
    app.config.from_object(config)
    app.config["SERVER_NAME"] = "xsslab_app:9090"
    
    # Initialize the db only once
    db.init_app(app)

    # Enregistrer les blueprints
    app.register_blueprint(scenarios_bp)
    app.register_blueprint(payloads_bp, url_prefix='/payloads')
    app.register_blueprint(results_bp, url_prefix='/results')
    # app.register_blueprint(auto_test_bp, url_prefix='/auto')
    app.register_blueprint(headless_test_bp, url_prefix='/auto_headless')


    # Synchronize scenarios with database
    with app.app_context():
        db.create_all()  # Ensure all tables exist before syncing
        sync_scenarios_to_db()

    @app.route('/')
    def index():
        last_scenario = Scenario.query.order_by(Scenario.id.desc()).first()
        payloads = Payload.query.all()
        payloads_data = [{"id": p.id, "payload": p.content} for p in payloads]
        return render_template('index.html', last_scenario=last_scenario, payloads=payloads_data)

    return app

if __name__ == '__main__':
    # Lancer en debug ou en prod
    app = create_app()
    
    # Retry logic for DB connection
    for attempt in range(1, MAX_DB_RETRIES + 1):
        try:
            with app.app_context():
                with db.engine.connect() as conn:
                    conn.execute(text('SELECT 1'))
            print("[DB INIT] Database connection successful.")
            break
        except OperationalError as e:
            print(f"[DB INIT] Attempt {attempt}/{MAX_DB_RETRIES} failed: {e}")
            if attempt == MAX_DB_RETRIES:
                print("[DB INIT] Max retries reached. Exiting.")
                raise
            time.sleep(RETRY_DELAY)
    
    app.run(host='0.0.0.0', port=9090, debug=True, use_reloader=True)
