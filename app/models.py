from db import db
from datetime import datetime

class Scenario(db.Model):
    __tablename__ = "scenarios"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    # On peut ajouter d'autres champs (type, etc.)

class Payload(db.Model):
    __tablename__ = "payloads"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    size = db.Column(db.Integer, default=0)
    # On pourrait stocker la date d'upload, etc.

class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenarios.id'))
    payload_id = db.Column(db.Integer, db.ForeignKey('payloads.id'))
    triggered = db.Column(db.Boolean, default=False)  # XSS déclenché ?
    regex_matches = db.Column(db.Integer, default=0)   # nb de patterns détectés
    test_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    scenario = db.relationship('Scenario', backref='results')
    payload = db.relationship('Payload', backref='results')
