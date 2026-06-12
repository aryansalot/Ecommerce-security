from app import db
from datetime import datetime

class Threat(db.Model):
    __tablename__ = 'threats'
    
    id = db.Column(db.Integer, primary_key=True)
    threat_id = db.Column(db.String(50), unique=True, nullable=False)
    threat_name = db.Column(db.String(255), nullable=False)
    threat_type = db.Column(db.String(50))  # malware, ransomware, APT, botnet
    ioc_type = db.Column(db.String(50))  # ip, domain, hash, email
    ioc_value = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(20))  # Critical, High, Medium, Low
    source = db.Column(db.String(255))
    status = db.Column(db.String(50), default='active')  # active, mitigated, resolved
    description = db.Column(db.Text)
    detected_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime)
    tags = db.Column(db.String(255))
    confidence = db.Column(db.Integer, default=75)  # 0-100
    
    def to_dict(self):
        return {
            'id': self.id,
            'threat_id': self.threat_id,
            'threat_name': self.threat_name,
            'threat_type': self.threat_type,
            'ioc_type': self.ioc_type,
            'ioc_value': self.ioc_value,
            'severity': self.severity,
            'source': self.source,
            'status': self.status,
            'description': self.description,
            'detected_date': self.detected_date.isoformat() if self.detected_date else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'tags': self.tags,
            'confidence': self.confidence
        }
