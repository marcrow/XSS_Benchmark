from flask import Blueprint, render_template, request
from models import Scenario, Payload, Result, db
from scenarios.basic_scenarios import basic_scenarios

scenarios_bp = Blueprint('scenarios_bp', __name__)

@scenarios_bp.route('/scenarios', methods=['GET'])
def list_scenarios():
    # Récupérer en base et ordonner par ID
    scenarios = Scenario.query.order_by(Scenario.id.asc()).all()
    return render_template("scenarios_list.html", scenarios=scenarios)

@scenarios_bp.route('/scenario/<int:scenario_id>', methods=['GET'])
def show_scenario(scenario_id):
    scenario = Scenario.query.get_or_404(scenario_id)
    # Hypothèse : On récupère le payloadID en param ou un "dernier" payload pour la démo
    payload_id = request.args.get('payload_id', type=int)
    payload = Payload.query.get(payload_id) if payload_id else None

    # On injecte ce payload dans la page, selon la logique du scenario
    # On peut faire un template distinct ou un template unique avec un switch
    return render_template(
        "scenario_template.html",
        scenario=scenario,
        payload=payload
    )
