from flask import Blueprint, request, jsonify
from models import Result, db, Payload, Scenario
from .payloads_controller import detect_regex
import datetime

results_bp = Blueprint('results_bp', __name__)

@results_bp.route('/report_not_triggered', methods=['POST'])
def report_not_triggered():
    """
    Endpoint to log that a scenario/payload did NOT trigger XSS.
    Expects scenario_id and payload_id as POST data.
    """
    scenario_id = request.form.get('scenario_id', type=int)
    payload_id = request.form.get('payload_id', type=int)
    if not scenario_id or not payload_id:
        return "Missing parameters", 400

    # Check if a result already exists
    result = Result.query.filter_by(scenario_id=scenario_id, payload_id=payload_id).first()
    if not result:
        result = Result(scenario_id=scenario_id, payload_id=payload_id)
    
    result.triggered = False
    result.test_timestamp = datetime.datetime.utcnow()
    result.regex_matches = 0
    
    db.session.add(result)
    db.session.commit()
    
    return "Not triggered logged", 200

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
def scoreboard():
    """
    Retourne les enregistrements de la table Results en JSON.
    Affiche aussi les scénarios "pending" (pas encore de résultat pour ce payload).
    """
    payload_id = request.args.get('payload_id', type=int)
    # Si pas de payload_id, fallback à l'ancien comportement (tous les résultats)
    if not payload_id:
        results = Result.query.all()
        data = []
        for r in results:
            data.append({
                "scenario_id": r.scenario_id,
                "scenario_name": r.scenario.name if r.scenario else "",
                "payload_id": r.payload_id,
                "payload_size": r.payload.size if r.payload else 0,
                "status": "done" if r.triggered else "not_triggered",
                "triggered": "Yes" if r.triggered else "No",
                "regex_matches": r.regex_matches,
                "test_timestamp": r.test_timestamp.isoformat() if r.test_timestamp else ""
            })
        return jsonify(data)

    # Sinon, on veut le scoreboard pour un payload précis
    scenarios = Scenario.query.all()
    data = []
    for s in scenarios:
        result = Result.query.filter_by(scenario_id=s.id, payload_id=payload_id).first()
        if result:
            status = "done" if result.triggered else "not_triggered"
            triggered = "Yes" if result.triggered else "No"
            regex_matches = result.regex_matches
            test_timestamp = result.test_timestamp.isoformat() if result.test_timestamp else ""
        else:
            status = "pending"
            triggered = "Pending"
            regex_matches = 0
            test_timestamp = ""
        data.append({
            "scenario_id": s.id,
            "scenario_name": s.name,
            "payload_id": payload_id,
            "payload_size": Payload.query.get(payload_id).size if Payload.query.get(payload_id) else 0,
            "status": status,
            "triggered": triggered,
            "regex_matches": regex_matches,
            "test_timestamp": test_timestamp
        })
    return jsonify(data)


@results_bp.route('/report_md', methods=['GET'])
def report_markdown():
    payload_id = request.args.get('payload_id', type=int)
    if not payload_id:
        return "Missing ?payload_id=", 400

    results = Result.query.filter_by(payload_id=payload_id).all()
    if not results:
        return "No result for this payload", 404

    payload = Payload.query.get(payload_id)
    total = len(results)
    triggered = sum(1 for r in results if r.triggered)

    lines = []
    lines.append(f"# bXSS Report - Payload #{payload_id}")
    lines.append(f"**Date :** {datetime.datetime.utcnow().isoformat()}")
    lines.append(f"**Payload :** `{payload.content}`")
    lines.append(f"**Score :** {triggered} / {total} ({round(triggered/total*100)}%)")
    lines.append(f"**Length :** {payload.size}")
    lines.append(f"**Number of regex triggers by the payload (less is better):** {results[0].regex_matches}\n")


    lines.append("## Scenarios details")
    lines.append("|Scenario|ID|Triggered|Regex Match|Timestamp|")
    lines.append("|---|---|---|---|---|")

    for r in results:
        lines.append(f"|{r.scenario.name}|{r.scenario_id}|{'✅' if r.triggered else '❌'}|{r.regex_matches}|{r.test_timestamp.strftime('%Y-%m-%d %H:%M:%S')}|")

    return "\n".join(lines), 200, {"Content-Type": "text/markdown; charset=utf-8"}

