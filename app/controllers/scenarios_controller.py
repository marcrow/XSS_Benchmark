from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from models import Payload, Scenario
from scenarios.loader import get_scenario_by_id, get_all_scenarios

scenarios_bp = Blueprint('scenarios_bp', __name__)

@scenarios_bp.route('/scenarios', methods=['GET'])
def list_scenarios():
    # Get scenarios from DB
    scenarios = Scenario.query.all()
    return render_template("scenarios_list.html", scenarios=scenarios)

@scenarios_bp.route('/scenarios/sync', methods=['POST'])
def sync_scenarios():
    from scenarios.sync import sync_scenarios_to_db
    sync_scenarios_to_db()
    flash("Scenarios synced from YAML!", "success")
    return redirect(url_for('scenarios_bp.list_scenarios'))

@scenarios_bp.route('/scenario/<int:scenario_id>', methods=['GET'])
def show_scenario(scenario_id):
    scenario = Scenario.query.get(scenario_id)
    if not scenario:
        abort(404, "Scenario not found")
    
    payload_id = request.args.get('payload_id', type=int)
    payload = Payload.query.get(payload_id) if payload_id else None
    
    return render_template(
        "scenario_template.html",
        scenario=scenario,
        payload=payload
    )
