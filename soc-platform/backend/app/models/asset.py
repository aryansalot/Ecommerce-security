from app import db
from datetime import datetime

class Asset(db.Model):
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String(50), unique=True, nullable=False)
    asset_name = db.Column(db.String(255), nullable=False)
    asset_type = db.Column(db.String(50))  # server, database, application, endpoint
    ip_address = db.Column(db.String(50))
    hostname = db.Column(db.String(255))
    os = db.Column(db.String(100))
    status = db.Column(db.String(50), default='active')  # active, inactive, decommissioned
    criticality = db.Column(db.String(50))  # Critical, High, Medium, Low
    vulnerabilities = db.Column(db.Integer, default=0)
    owner = db.Column(db.String(120))
    last_scan = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'asset_name': self.asset_name,
            'asset_type': self.asset_type,
            'ip_address': self.ip_address,
            'hostname': self.hostname,
            'os': self.os,
            'status': self.status,
            'criticality': self.criticality,
            'vulnerabilities': self.vulnerabilities,
            'owner': self.owner,
            'last_scan': self.last_scan.isoformat() if self.last_scan else None,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'tags': self.tags
        }
