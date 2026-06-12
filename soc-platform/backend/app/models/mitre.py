from app import db
from datetime import datetime

class MitreAttack(db.Model):
    __tablename__ = 'mitre_attacks'
    
    id = db.Column(db.Integer, primary_key=True)
    technique_id = db.Column(db.String(50), unique=True, nullable=False)  # T1234
    tactic = db.Column(db.String(100), nullable=False)
    technique = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    platforms = db.Column(db.String(255))
    detection_count = db.Column(db.Integer, default=0)
    mitigation = db.Column(db.Text)
    references = db.Column(db.Text)
    last_detected = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'technique_id': self.technique_id,
            'tactic': self.tactic,
            'technique': self.technique,
            'description': self.description,
            'platforms': self.platforms,
            'detection_count': self.detection_count,
            'mitigation': self.mitigation,
            'references': self.references,
            'last_detected': self.last_detected.isoformat() if self.last_detected else None,
            'created_date': self.created_date.isoformat() if self.created_date else None
        }
