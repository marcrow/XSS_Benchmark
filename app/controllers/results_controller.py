from flask import Blueprint, request, jsonify
from models import Result, db, Payload, Scenario
from .payloads_controller import detect_regex
import datetime

results_bp = Blueprint('results_bp', __name__)

@results_bp.route('/report', methods=['GET', 'POST'])
def report_xss():
    """
    Appelé par le script si la charge XSS s'est exécutée.
    ex: /report?scenario_id=1&payload_id=42
    """
    scenario_id = request.args.get('scenario_id', type=int)
    payload_id = request.args.get('payload_id', type=int)
    if not scenario_id or not payload_id:
        return "Missing parameters", 400

    # Chercher un record existant ou en créer un
    result = Result.query.filter_by(scenario_id=scenario_id, payload_id=payload_id).first()
    if not result:
        result = Result(scenario_id=scenario_id, payload_id=payload_id)

    result.triggered = True
    result.test_timestamp = datetime.datetime.utcnow()

    # calculer regex
    payload = Payload.query.get(payload_id)
    nb_matches = detect_regex(payload.content) if payload else 0
    result.regex_matches = nb_matches

    db.session.add(result)
    db.session.commit()

    return "XSS Triggered logged", 200


@results_bp.route('/scoreboard', methods=['GET'])
@results_bp.route('/scoreboard', methods=['GET'])
def scoreboard():
    """
    Retourne les enregistrements de la table Results en JSON.
    """
    results = Result.query.all()
    data = []
    for r in results:
        data.append({
            "scenario_id": r.scenario_id,
            "scenario_name": r.scenario.name if r.scenario else "",
            "payload_id": r.payload_id,
            "payload_size": r.payload.size if r.payload else 0,
            # On peut convertir le booléen triggered en string:
            "triggered": "Yes" if r.triggered else "No",
            "regex_matches": r.regex_matches,
            "test_timestamp": r.test_timestamp.isoformat() if r.test_timestamp else ""
        })
    return jsonify(data)


@results_bp.route('/report_md', methods=['GET'])
def report_markdown():
    """
    Génère un rapport Markdown plus propre.
    """
    results = Result.query.all()

    lines = []
    # Titre
    lines.append("# Rapport XSS\n")
    # En-tête de la table
    lines.append("|Scenario|Scenario ID|Payload ID|Triggered|RegexMatches|Size|Timestamp|")
    lines.append("|---|---|---|---|---|---|---|")

    for r in results:
        scenario_name = r.scenario.name if r.scenario else ""
        scenario_id = r.scenario_id
        payload_id = r.payload_id
        triggered = "Yes" if r.triggered else "No"
        regex_matches = r.regex_matches
        size = r.payload.size if r.payload else 0
        timestamp = r.test_timestamp.isoformat() if r.test_timestamp else ""

        row = f"|{scenario_name}|{scenario_id}|{payload_id}|{triggered}|{regex_matches}|{size}|{timestamp}|"
        lines.append(row)

    # Pour forcer l'affichage en tant que "plain text" (utile dans un navigateur)
    md_output = "\n".join(lines)
    return md_output, 200, {"Content-Type": "text/plain; charset=utf-8"}
