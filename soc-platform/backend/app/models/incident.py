from app import db
from datetime import datetime

class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))  # Critical, High, Medium, Low
    status = db.Column(db.String(50), default='open')  # open, investigating, contained, resolved
    affected_systems = db.Column(db.Text)  # JSON string
    root_cause = db.Column(db.Text)
    impact = db.Column(db.String(255))
    timeline = db.Column(db.Text)  # JSON string
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    detected_date = db.Column(db.DateTime)
    resolved_date = db.Column(db.DateTime)
    assigned_to = db.Column(db.String(120))
    response_time = db.Column(db.Integer)  # minutes
    
    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'status': self.status,
            'affected_systems': self.affected_systems,
            'root_cause': self.root_cause,
            'impact': self.impact,
            'timeline': self.timeline,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'detected_date': self.detected_date.isoformat() if self.detected_date else None,
            'resolved_date': self.resolved_date.isoformat() if self.resolved_date else None,
            'assigned_to': self.assigned_to,
            'response_time': self.response_time
        }
