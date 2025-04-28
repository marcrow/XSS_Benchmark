from flask import Blueprint, request, redirect, url_for, render_template
from models import Payload, Result, Scenario, db
import re

payloads_bp = Blueprint('payloads_bp', __name__)

# Exemple de patterns
REGEX_PATTERNS = [
    r"<script[^>]*>",   # simple
    r"on\w+=.*",        # attribut d'event
    r".*javascript:.*",   # URL javascript
    # ... on peut en ajouter d'autres
]

@payloads_bp.route('/upload_payload', methods=['POST'])
def upload_payload():
    content = request.form.get('payload')
    if not content:
        return "No payload provided", 400

    p = Payload(content=content, size=len(content))
    db.session.add(p)
    db.session.commit()

    # Redirection vers la page qui liste les payloads
    return redirect(url_for('payloads_bp.list_payloads'))

@payloads_bp.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    lines = file.read().decode('utf-8', errors='ignore').splitlines()
    for line in lines:
        line = line.strip()
        if line:
            p = Payload(content=line, size=len(line))
            db.session.add(p)
    db.session.commit()

    return redirect(url_for('payloads_bp.list_payloads'))

@payloads_bp.route('/payloads', methods=['GET'])
def list_payloads():
    payloads = Payload.query.order_by(Payload.id.asc()).all()
    nb_scenarios = Scenario.query.count()
    payloads_data = []
    for p in payloads:
        # Count results with triggered=True for this payload
        nb_triggered = Result.query.filter_by(payload_id=p.id, triggered=True).count()
        # Check if any test exists for this payload
        test_exists = Result.query.filter_by(payload_id=p.id).count() > 0
        score = f"{nb_triggered}/{nb_scenarios}" if nb_scenarios > 0 else "0/0"
        report_link = url_for('results_bp.report_markdown', payload_id=p.id) if test_exists else "#"
        payloads_data.append({
            "id": p.id,
            "payload": p.content,
            "score": score,
            "report_link": report_link,
            "test_exists": test_exists
        })
    return render_template("payloads.html", payloads=payloads_data)

def detect_regex(payload_content: str) -> int:
    """Retourne le nombre de patterns qui matchent."""
    count = 0
    for pattern in REGEX_PATTERNS:
        if re.search(pattern, payload_content, flags=re.IGNORECASE):
            count += 1
    return count
