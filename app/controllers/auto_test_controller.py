# app/controllers/auto_test_controller.py
from flask import Blueprint, jsonify
import time
import requests
from models import Scenario
# Si vous avez un config ou quelque chose pour connaître l'adresse locale

auto_test_bp = Blueprint('auto_test_bp', __name__)

@auto_test_bp.route('/run_all', methods=['GET'])
def run_all_scenarios():
    """
    Teste tous les scénarios avec un payload_id donné en param
    ex: /run_all?payload_id=3
    """
    from flask import request

    payload_id = request.args.get("payload_id", type=int)
    if not payload_id:
        return "Missing ?payload_id=", 400

    # Récupère tous les scénarios en DB
    scenario_list = Scenario.query.all()
    
    # On suppose que l'app écoute en interne sur http://app:8080 ou
    # qu'on peut y accéder via http://localhost:8080 si tout est dans Docker
    # Si le conteneur "app" n'est pas accessible depuis l'intérieur, on met l'URL correspondante.
    base_url = "http://xsslab_app:9090"

    results = []
    for s in scenario_list:
        scenario_url = f"{base_url}/scenario/{s.id}?payload_id={payload_id}"

        # On fait une requête GET
        try:
            resp = requests.get(scenario_url, timeout=3)
            status = resp.status_code
            results.append({
                "scenario_id": s.id,
                "scenario_name": s.name,
                "url_visited": scenario_url,
                "status": status
            })
            # Attendre un peu si besoin que le XSS se déclenche
            time.sleep(0.5)  
        except Exception as e:
            results.append({
                "scenario_id": s.id,
                "scenario_name": s.name,
                "url_visited": scenario_url,
                "error": str(e)
            })

    # Ensuite, on peut récupérer le scoreboard en JSON
    scoreboard_url = f"{base_url}/results/scoreboard"
    scoreboard_data = []
    try:
        resp_sb = requests.get(scoreboard_url, timeout=3)
        scoreboard_data = resp_sb.json()
    except Exception as e:
        scoreboard_data = {"error": str(e)}

    return jsonify({
        "visited": results,
        "scoreboard": scoreboard_data
    })
