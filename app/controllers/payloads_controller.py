from flask import Blueprint, request, redirect, url_for
from models import Payload, db
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
    payloads = Payload.query.all()
    return """<h1>List of Payloads</h1>""" + "<br>".join([f"{{p.id}} - {{p.content}}" for p in payloads])

def detect_regex(payload_content: str) -> int:
    """Retourne le nombre de patterns qui matchent."""
    count = 0
    for pattern in REGEX_PATTERNS:
        if re.search(pattern, payload_content, flags=re.IGNORECASE):
            count += 1
    return count
