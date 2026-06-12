from app import db
from datetime import datetime

class ComplianceStatus(db.Model):
    __tablename__ = 'compliance_status'
    
    id = db.Column(db.Integer, primary_key=True)
    framework = db.Column(db.String(50), nullable=False)  # PCI-DSS, HIPAA, SOC2, CIS, OWASP
    requirement = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50))  # Compliant, Non-Compliant, In-Progress
    score = db.Column(db.Float, default=0.0)
    findings = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    remediation = db.Column(db.Text)
    target_date = db.Column(db.DateTime)
    last_assessed = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_to = db.Column(db.String(120))
    
    def to_dict(self):
        return {
            'id': self.id,
            'framework': self.framework,
            'requirement': self.requirement,
            'status': self.status,
            'score': self.score,
            'findings': self.findings,
            'description': self.description,
            'remediation': self.remediation,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'last_assessed': self.last_assessed.isoformat() if self.last_assessed else None,
            'assigned_to': self.assigned_to
        }
