from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.risk_service import RiskScoringEngine, ComplianceCalculator
from app.models import Vulnerability, Asset

bp = Blueprint('risk', __name__, url_prefix='/api/risk')

@bp.route('/score', methods=['GET'])
@jwt_required()
def get_risk_score():
    """Get organizational risk score"""
    try:
        risk_score = RiskScoringEngine.calculate_organizational_risk_score()
        recommendations = RiskScoringEngine.get_risk_recommendations(risk_score)
        
        return jsonify({
            'risk_score': risk_score,
            'risk_level': 'Critical' if risk_score >= 80 else 'High' if risk_score >= 60 else 'Medium' if risk_score >= 40 else 'Low',
            'recommendations': recommendations
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/heatmap', methods=['GET'])
@jwt_required()
def get_risk_heatmap():
    """Get risk heatmap data"""
    try:
        heatmap_data = RiskScoringEngine.get_risk_heatmap_data()
        
        return jsonify(heatmap_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/scorecard', methods=['GET'])
@jwt_required()
def get_security_scorecard():
    """Get security scorecard"""
    try:
        risk_score = RiskScoringEngine.calculate_organizational_risk_score()
        compliance_score = ComplianceCalculator.get_overall_compliance_score()
        
        vulnerabilities = Vulnerability.query.all()
        vuln_risk = sum([RiskScoringEngine.calculate_vulnerability_risk_score(v) for v in vulnerabilities])
        vuln_avg = (vuln_risk / len(vulnerabilities)) if vulnerabilities else 0
        
        assets = Asset.query.all()
        asset_scores = [RiskScoringEngine.calculate_asset_risk_score(a) for a in assets]
        asset_avg = sum(asset_scores) / len(asset_scores) if asset_scores else 0
        
        scorecard = {
            'overall_score': (risk_score + compliance_score + vuln_avg + asset_avg) / 4,
            'security_maturity': (100 - risk_score),
            'compliance_readiness': compliance_score,
            'risk_exposure': risk_score,
            'asset_health': asset_avg
        }
        
        return jsonify(scorecard), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/asset/<int:asset_id>', methods=['GET'])
@jwt_required()
def get_asset_risk(asset_id):
    """Get asset risk score"""
    try:
        asset = Asset.query.get(asset_id)
        
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        risk_score = RiskScoringEngine.calculate_asset_risk_score(asset)
        
        return jsonify({
            'asset_id': asset.id,
            'asset_name': asset.asset_name,
            'risk_score': risk_score,
            'risk_level': 'Critical' if risk_score >= 80 else 'High' if risk_score >= 60 else 'Medium' if risk_score >= 40 else 'Low'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
