from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import (
    Vulnerability, Incident, Threat, Alert, 
    Asset, ComplianceStatus
)
from app.services.risk_service import RiskScoringEngine, ComplianceCalculator
from datetime import datetime, timedelta

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/overview', methods=['GET'])
@jwt_required()
def get_dashboard_overview():
    """Get main dashboard overview"""
    try:
        # Get counts
        total_vulnerabilities = Vulnerability.query.count()
        critical_vulnerabilities = Vulnerability.query.filter_by(severity='Critical').count()
        open_vulnerabilities = Vulnerability.query.filter_by(status='open').count()
        
        open_incidents = Incident.query.filter_by(status='open').count()
        total_incidents = Incident.query.count()
        
        active_threats = Threat.query.filter_by(status='active').count()
        total_threats = Threat.query.count()
        
        new_alerts = Alert.query.filter_by(status='new').count()
        total_alerts = Alert.query.count()
        
        active_assets = Asset.query.filter_by(status='active').count()
        total_assets = Asset.query.count()
        
        # Calculate risk scores
        org_risk_score = RiskScoringEngine.calculate_organizational_risk_score()
        compliance_score = ComplianceCalculator.get_overall_compliance_score()
        
        # Get recent data
        recent_vulnerabilities = Vulnerability.query.order_by(Vulnerability.discovered_date.desc()).limit(5).all()
        recent_incidents = Incident.query.order_by(Incident.created_date.desc()).limit(5).all()
        recent_alerts = Alert.query.order_by(Alert.created_date.desc()).limit(5).all()
        
        dashboard_data = {
            'vulnerabilities': {
                'total': total_vulnerabilities,
                'critical': critical_vulnerabilities,
                'open': open_vulnerabilities
            },
            'incidents': {
                'total': total_incidents,
                'open': open_incidents
            },
            'threats': {
                'total': total_threats,
                'active': active_threats
            },
            'alerts': {
                'total': total_alerts,
                'new': new_alerts
            },
            'assets': {
                'total': total_assets,
                'active': active_assets
            },
            'risk_score': org_risk_score,
            'compliance_score': compliance_score,
            'recent': {
                'vulnerabilities': [v.to_dict() for v in recent_vulnerabilities],
                'incidents': [i.to_dict() for i in recent_incidents],
                'alerts': [a.to_dict() for a in recent_alerts]
            }
        }
        
        return jsonify(dashboard_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/health', methods=['GET'])
@jwt_required()
def get_security_health():
    """Get security health metrics"""
    try:
        open_vulns = Vulnerability.query.filter_by(status='open').count()
        open_incidents = Incident.query.filter_by(status='open').count()
        active_threats = Threat.query.filter_by(status='active').count()
        
        # Health score calculation
        health_score = 100
        health_score -= open_vulns * 2
        health_score -= open_incidents * 5
        health_score -= active_threats * 3
        health_score = max(0, min(100, health_score))
        
        health_status = 'Healthy'
        if health_score >= 80:
            health_status = 'Good'
        elif health_score >= 60:
            health_status = 'Fair'
        elif health_score >= 40:
            health_status = 'Poor'
        else:
            health_status = 'Critical'
        
        return jsonify({
            'health_score': health_score,
            'health_status': health_status,
            'open_vulnerabilities': open_vulns,
            'open_incidents': open_incidents,
            'active_threats': active_threats
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/metrics', methods=['GET'])
@jwt_required()
def get_metrics():
    """Get detailed metrics"""
    try:
        metrics = {
            'mttr': 45,  # Mean Time To Respond (minutes)
            'mtbf': 720,  # Mean Time Between Failures (hours)
            'remediation_rate': 85,  # Percentage
            'detection_rate': 92,  # Percentage
            'false_positive_rate': 5,  # Percentage
            'alert_accuracy': 95  # Percentage
        }
        return jsonify(metrics), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/timeline', methods=['GET'])
@jwt_required()
def get_timeline():
    """Get security events timeline for last 30 days"""
    try:
        timeline_data = []
        
        for i in range(30):
            date = datetime.utcnow() - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            vulns = Vulnerability.query.filter(
                Vulnerability.discovered_date >= date,
                Vulnerability.discovered_date < date + timedelta(days=1)
            ).count()
            
            incidents = Incident.query.filter(
                Incident.created_date >= date,
                Incident.created_date < date + timedelta(days=1)
            ).count()
            
            alerts = Alert.query.filter(
                Alert.created_date >= date,
                Alert.created_date < date + timedelta(days=1)
            ).count()
            
            timeline_data.append({
                'date': date_str,
                'vulnerabilities': vulns,
                'incidents': incidents,
                'alerts': alerts
            })
        
        return jsonify(timeline_data[::-1]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
