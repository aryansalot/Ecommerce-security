from app import db
from datetime import datetime

class Alert(db.Model):
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))  # Critical, High, Medium, Low, Info
    source = db.Column(db.String(255))
    category = db.Column(db.String(100))
    status = db.Column(db.String(50), default='new')  # new, acknowledged, in_progress, resolved
    affected_resource = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged_date = db.Column(db.DateTime)
    resolved_date = db.Column(db.DateTime)
    assigned_to = db.Column(db.String(120))
    details = db.Column(db.Text)  # JSON string
    
    def to_dict(self):
        return {
            'id': self.id,
            'alert_id': self.alert_id,
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'source': self.source,
            'category': self.category,
            'status': self.status,
            'affected_resource': self.affected_resource,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'acknowledged_date': self.acknowledged_date.isoformat() if self.acknowledged_date else None,
            'resolved_date': self.resolved_date.isoformat() if self.resolved_date else None,
            'assigned_to': self.assigned_to,
            'details': self.details
        }
