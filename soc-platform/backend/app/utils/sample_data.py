from app import db
from app.models import (
    User, Vulnerability, Incident, Threat, Alert, 
    ComplianceStatus, MitreAttack, Asset, AuditLog
)
from datetime import datetime, timedelta
import random

def initialize_sample_data():
    """
    Initialize database with sample data if empty
    """
    
    # Check if data already exists
    if User.query.first() is not None:
        return
    
    # Create sample users
    admin_user = User(
        username='admin',
        email='admin@soc-platform.com',
        first_name='Admin',
        last_name='User',
        role='admin',
        department='Security',
        active=True
    )
    admin_user.set_password('admin123')
    
    manager_user = User(
        username='manager',
        email='manager@soc-platform.com',
        first_name='Manager',
        last_name='User',
        role='manager',
        department='SOC',
        active=True
    )
    manager_user.set_password('manager123')
    
    analyst_user = User(
        username='analyst',
        email='analyst@soc-platform.com',
        first_name='Analyst',
        last_name='User',
        role='analyst',
        department='SOC',
        active=True
    )
    analyst_user.set_password('analyst123')
    
    db.session.add_all([admin_user, manager_user, analyst_user])
    db.session.commit()
    
    # Create sample assets
    assets_data = [
        ('web-server-01', 'Production Web Server', 'server', '192.168.1.10', 'web-prod-01', 'Linux', 'Critical'),
        ('db-server-01', 'Production Database', 'database', '192.168.1.20', 'db-prod-01', 'Linux', 'Critical'),
        ('app-server-01', 'Application Server', 'server', '192.168.1.30', 'app-prod-01', 'Windows', 'High'),
        ('endpoint-001', 'Workstation 1', 'endpoint', '192.168.1.100', 'WORKSTATION-001', 'Windows', 'Medium'),
        ('api-gateway', 'API Gateway', 'application', '192.168.1.40', 'api-gateway-01', 'Linux', 'Critical'),
    ]
    
    created_assets = []
    for i, (asset_id, name, atype, ip, hostname, os, crit) in enumerate(assets_data, 1):
        asset = Asset(
            asset_id=asset_id,
            asset_name=name,
            asset_type=atype,
            ip_address=ip,
            hostname=hostname,
            os=os,
            status='active',
            criticality=crit,
            vulnerabilities=random.randint(0, 10),
            owner='Security Team',
            last_scan=datetime.utcnow() - timedelta(days=random.randint(1, 7))
        )
        db.session.add(asset)
        created_assets.append(asset)
    db.session.commit()
    
    # Create sample vulnerabilities
    cves = [
        ('CVE-2024-0001', 'Remote Code Execution in Web Framework', 'A critical RCE vulnerability', 9.8, 'Critical'),
        ('CVE-2024-0002', 'SQL Injection in Application', 'SQL injection vulnerability in login form', 8.6, 'High'),
        ('CVE-2024-0003', 'Cross-Site Scripting (XSS)', 'DOM-based XSS in search functionality', 6.5, 'Medium'),
        ('CVE-2024-0004', 'Insufficient Authentication', 'Missing authentication on admin API', 8.2, 'High'),
        ('CVE-2024-0005', 'Hardcoded Credentials', 'Hardcoded database password in config', 7.5, 'High'),
        ('CVE-2024-0006', 'Missing Security Updates', 'Operating system patch not applied', 5.3, 'Medium'),
        ('CVE-2024-0007', 'Weak Encryption', 'Outdated TLS version in use', 7.8, 'High'),
        ('CVE-2024-0008', 'Information Disclosure', 'Sensitive data exposed in error messages', 4.2, 'Low'),
    ]
    
    for cve_id, title, desc, cvss, severity in cves:
        vuln = Vulnerability(
            cve_id=cve_id,
            title=title,
            description=desc,
            cvss_score=cvss,
            severity=severity,
            affected_asset=random.choice([a.asset_name for a in created_assets]),
            status=random.choice(['open', 'open', 'open', 'mitigated']),
            remediation='Apply security patches and updates',
            discovered_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            assigned_to='Security Team',
            priority=random.randint(1, 10)
        )
        db.session.add(vuln)
    db.session.commit()
    
    # Create sample incidents
    incidents_data = [
        ('INC-2024-001', 'Unauthorized Access Attempt', 'Multiple failed login attempts detected', 'High', 'open'),
        ('INC-2024-002', 'Malware Detection', 'Trojan detected on endpoint', 'Critical', 'investigating'),
        ('INC-2024-003', 'Data Exfiltration', 'Suspicious data transfer to external IP', 'Critical', 'investigating'),
        ('INC-2024-004', 'Network Anomaly', 'Unusual network traffic pattern detected', 'Medium', 'resolved'),
        ('INC-2024-005', 'Privilege Escalation', 'Unauthorized privilege escalation detected', 'High', 'contained'),
    ]
    
    for inc_id, title, desc, severity, status in incidents_data:
        incident = Incident(
            incident_id=inc_id,
            title=title,
            description=desc,
            severity=severity,
            status=status,
            affected_systems=random.choice([a.asset_name for a in created_assets]),
            root_cause='Under investigation',
            impact='Potential data breach',
            created_date=datetime.utcnow() - timedelta(days=random.randint(0, 15)),
            detected_date=datetime.utcnow() - timedelta(days=random.randint(0, 15)),
            assigned_to='Security Team',
            response_time=random.randint(15, 120)
        )
        db.session.add(incident)
    db.session.commit()
    
    # Create sample threats
    threats_data = [
        ('THR-2024-001', 'EMOTET', 'malware', 'ip', '192.0.2.1', 'Critical', 'OSINT', 'Emotet banking trojan', 92),
        ('THR-2024-002', 'MIRAI', 'botnet', 'ip', '198.51.100.5', 'High', 'Threat Feed', 'Mirai botnet node', 85),
        ('THR-2024-003', 'Phishing Campaign', 'malware', 'domain', 'phishing-campaign.com', 'High', 'OSINT', 'Phishing domain', 78),
        ('THR-2024-004', 'APT28 Hash', 'APT', 'hash', 'd41d8cd98f00b204e9800998ecf8427e', 'Critical', 'MISP', 'APT28 malware sample', 95),
        ('THR-2024-005', 'Ransomware Variant', 'ransomware', 'ip', '203.0.113.42', 'Critical', 'Threat Feed', 'LockBit ransomware C2', 88),
    ]
    
    for threat_id, name, ttype, ioc_type, ioc_value, severity, source, desc, confidence in threats_data:
        threat = Threat(
            threat_id=threat_id,
            threat_name=name,
            threat_type=ttype,
            ioc_type=ioc_type,
            ioc_value=ioc_value,
            severity=severity,
            source=source,
            status='active',
            description=desc,
            detected_date=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            tags='malicious,monitored',
            confidence=confidence
        )
        db.session.add(threat)
    db.session.commit()
    
    # Create sample alerts
    for i in range(1, 11):
        alert = Alert(
            alert_id=f'ALR-2024-{i:04d}',
            title=f'Security Alert #{i}',
            description=f'Alert description for security event {i}',
            severity=random.choice(['Critical', 'High', 'Medium', 'Low', 'Info']),
            source=random.choice(['IDS', 'Firewall', 'SIEM', 'EDR']),
            category=random.choice(['Network', 'Host', 'Application', 'User']),
            status=random.choice(['new', 'acknowledged', 'in_progress']),
            affected_resource=random.choice([a.asset_name for a in created_assets]),
            created_date=datetime.utcnow() - timedelta(hours=random.randint(0, 72)),
            assigned_to='Security Team'
        )
        db.session.add(alert)
    db.session.commit()
    
    # Create sample compliance statuses
    compliance_data = [
        ('PCI-DSS', 'Requirement 1: Install firewall', 'Compliant'),
        ('PCI-DSS', 'Requirement 2: Default passwords', 'Compliant'),
        ('PCI-DSS', 'Requirement 6: Security patches', 'Non-Compliant'),
        ('HIPAA', 'Encryption of data at rest', 'Compliant'),
        ('HIPAA', 'Access controls', 'In-Progress'),
        ('SOC2', 'Change management', 'Compliant'),
        ('SOC2', 'Incident response', 'In-Progress'),
        ('CIS', 'Inventory and control', 'Non-Compliant'),
        ('CIS', 'Secure configuration', 'Compliant'),
        ('OWASP', 'Broken Authentication', 'In-Progress'),
        ('OWASP', 'Injection', 'Compliant'),
    ]
    
    for framework, requirement, status in compliance_data:
        comp = ComplianceStatus(
            framework=framework,
            requirement=requirement,
            status=status,
            score=random.uniform(60, 100) if status == 'Compliant' else random.uniform(20, 60),
            findings=random.randint(0, 5) if status != 'Compliant' else 0,
            description=f'Compliance requirement: {requirement}',
            last_assessed=datetime.utcnow()
        )
        db.session.add(comp)
    db.session.commit()
    
    # Create sample MITRE ATT&CK techniques
    mitre_data = [
        ('T1566', 'Phishing', 'Initial Access', 'Adversaries may phish for initial access'),
        ('T1190', 'Exploit Public-Facing Application', 'Initial Access', 'Exploitation of public-facing applications'),
        ('T1059', 'Command and Scripting Interpreter', 'Execution', 'Execution via command line or scripts'),
        ('T1218', 'System Binary Proxy Execution', 'Defense Evasion', 'System binary proxy execution'),
        ('T1040', 'Network Sniffing', 'Discovery', 'Capture network traffic'),
        ('T1087', 'Account Discovery', 'Discovery', 'Enumerate user accounts'),
    ]
    
    for tech_id, technique, tactic, desc in mitre_data:
        mitre = MitreAttack(
            technique_id=tech_id,
            tactic=tactic,
            technique=technique,
            description=desc,
            platforms='Windows, Linux, macOS',
            detection_count=random.randint(0, 5),
            mitigation='Implement detection and response procedures'
        )
        db.session.add(mitre)
    db.session.commit()
    
    print("Sample data initialized successfully!")
