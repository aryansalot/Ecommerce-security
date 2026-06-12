import numpy as np
from app.models import Vulnerability, Incident, Threat, Asset, Alert

class RiskScoringEngine:
    """
    AI-powered risk scoring engine that calculates comprehensive security risk scores
    """
    
    @staticmethod
    def calculate_vulnerability_risk_score(vulnerability):
        """
        Calculate risk score for a vulnerability
        Factors: CVSS score, age, affected criticality, status
        """
        if not vulnerability:
            return 0
        
        # Base CVSS score (0-10)
        cvss_weight = (vulnerability.cvss_score / 10.0) * 40
        
        # Status weight - active vulnerabilities are riskier
        status_weight = {
            'open': 30,
            'mitigated': 10,
            'accepted': 15,
            'resolved': 0
        }
        status_score = status_weight.get(vulnerability.status, 20)
        
        # Priority weight
        priority_weight = (vulnerability.priority / 10.0) * 20
        
        # Severity multiplier
        severity_multiplier = {
            'Critical': 1.0,
            'High': 0.8,
            'Medium': 0.6,
            'Low': 0.3
        }
        multiplier = severity_multiplier.get(vulnerability.severity, 0.5)
        
        total_score = (cvss_weight + status_score + priority_weight) * multiplier
        return min(100, max(0, total_score))
    
    @staticmethod
    def calculate_asset_risk_score(asset):
        """
        Calculate risk score for an asset based on vulnerabilities and criticality
        """
        if not asset:
            return 0
        
        criticality_weight = {
            'Critical': 0.9,
            'High': 0.7,
            'Medium': 0.5,
            'Low': 0.2
        }
        
        criticality_score = criticality_weight.get(asset.criticality, 0.5) * 40
        
        # Vulnerability count
        vuln_score = min(asset.vulnerabilities * 5, 50)
        
        # Status weight
        status_weight = {
            'active': 10,
            'inactive': 2,
            'decommissioned': 0
        }
        status_score = status_weight.get(asset.status, 5)
        
        total_score = criticality_score + vuln_score + status_score
        return min(100, max(0, total_score))
    
    @staticmethod
    def calculate_organizational_risk_score():
        """
        Calculate overall organizational risk score
        """
        vulnerabilities = Vulnerability.query.all()
        incidents = Incident.query.filter_by(status='open').all()
        threats = Threat.query.filter_by(status='active').all()
        assets = Asset.query.filter_by(status='active').all()
        
        vuln_score = sum([RiskScoringEngine.calculate_vulnerability_risk_score(v) for v in vulnerabilities])
        vuln_avg = (vuln_score / len(vulnerabilities)) if vulnerabilities else 0
        
        incident_weight = len(incidents) * 15
        threat_weight = len(threats) * 10
        
        asset_scores = [RiskScoringEngine.calculate_asset_risk_score(a) for a in assets]
        asset_avg = sum(asset_scores) / len(asset_scores) if asset_scores else 0
        
        total = (vuln_avg * 0.4) + (incident_weight * 0.3) + (threat_weight * 0.2) + (asset_avg * 0.1)
        
        return min(100, max(0, total))
    
    @staticmethod
    def get_risk_recommendations(risk_score):
        """
        Generate recommendations based on risk score
        """
        recommendations = []
        
        if risk_score >= 80:
            recommendations = [
                "CRITICAL: Implement immediate incident response procedures",
                "Escalate to C-level security leadership",
                "Activate security war room",
                "Conduct emergency vulnerability assessment",
                "Review and strengthen access controls"
            ]
        elif risk_score >= 60:
            recommendations = [
                "HIGH: Accelerate critical vulnerability remediation",
                "Increase security monitoring and alerting",
                "Review compliance status",
                "Assess incident response capabilities",
                "Update threat intelligence feeds"
            ]
        elif risk_score >= 40:
            recommendations = [
                "MEDIUM: Schedule vulnerability remediation activities",
                "Review asset inventory and criticality",
                "Conduct security awareness training",
                "Update security policies",
                "Plan penetration testing"
            ]
        else:
            recommendations = [
                "LOW: Continue regular security operations",
                "Perform routine vulnerability scans",
                "Review and update security procedures",
                "Monitor threat landscape",
                "Maintain compliance posture"
            ]
        
        return recommendations
    
    @staticmethod
    def get_risk_heatmap_data():
        """
        Generate heatmap data for risk visualization
        """
        vulnerabilities = Vulnerability.query.all()
        incidents = Incident.query.all()
        threats = Threat.query.all()
        
        severity_counts = {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0
        }
        
        for vuln in vulnerabilities:
            severity_counts[vuln.severity] = severity_counts.get(vuln.severity, 0) + 1
        
        for incident in incidents:
            severity_counts[incident.severity] = severity_counts.get(incident.severity, 0) + 1
        
        for threat in threats:
            severity_counts[threat.severity] = severity_counts.get(threat.severity, 0) + 1
        
        return severity_counts

class ComplianceCalculator:
    """
    Calculates compliance scores and status
    """
    
    @staticmethod
    def calculate_compliance_score(framework):
        """
        Calculate compliance score for a specific framework
        """
        from app.models import ComplianceStatus
        
        statuses = ComplianceStatus.query.filter_by(framework=framework).all()
        
        if not statuses:
            return 0
        
        compliant_count = sum(1 for s in statuses if s.status == 'Compliant')
        total_count = len(statuses)
        
        score = (compliant_count / total_count) * 100 if total_count > 0 else 0
        return min(100, max(0, score))
    
    @staticmethod
    def get_overall_compliance_score():
        """
        Calculate overall compliance score across all frameworks
        """
        frameworks = ['PCI-DSS', 'HIPAA', 'SOC2', 'CIS', 'OWASP']
        scores = []
        
        for framework in frameworks:
            score = ComplianceCalculator.calculate_compliance_score(framework)
            scores.append(score)
        
        overall = sum(scores) / len(scores) if scores else 0
        return min(100, max(0, overall))
