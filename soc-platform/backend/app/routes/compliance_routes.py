from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import ComplianceStatus
from app.services.risk_service import ComplianceCalculator

bp = Blueprint('compliance', __name__, url_prefix='/api/compliance')

@bp.route('', methods=['GET'])
@jwt_required()
def get_compliance():
    """Get all compliance statuses"""
    try:
        framework = request.args.get('framework')
        
        query = ComplianceStatus.query
        
        if framework:
            query = query.filter_by(framework=framework)
        
        statuses = query.all()
        
        return jsonify([s.to_dict() for s in statuses]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/frameworks', methods=['GET'])
@jwt_required()
def get_frameworks():
    """Get compliance score by framework"""
    try:
        frameworks = ['PCI-DSS', 'HIPAA', 'SOC2', 'CIS', 'OWASP']
        scores = {}
        
        for framework in frameworks:
            scores[framework] = ComplianceCalculator.calculate_compliance_score(framework)
        
        return jsonify(scores), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/overall', methods=['GET'])
@jwt_required()
def get_overall_compliance():
    """Get overall compliance score"""
    try:
        overall_score = ComplianceCalculator.get_overall_compliance_score()
        
        return jsonify({
            'overall_compliance_score': overall_score,
            'status': 'Compliant' if overall_score >= 80 else 'Non-Compliant'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/matrix', methods=['GET'])
@jwt_required()
def get_compliance_matrix():
    """Get compliance matrix"""
    try:
        frameworks = ['PCI-DSS', 'HIPAA', 'SOC2', 'CIS', 'OWASP']
        matrix = {}
        
        for framework in frameworks:
            framework_reqs = ComplianceStatus.query.filter_by(framework=framework).all()
            matrix[framework] = {
                'total': len(framework_reqs),
                'compliant': sum(1 for r in framework_reqs if r.status == 'Compliant'),
                'non_compliant': sum(1 for r in framework_reqs if r.status == 'Non-Compliant'),
                'in_progress': sum(1 for r in framework_reqs if r.status == 'In-Progress'),
                'score': ComplianceCalculator.calculate_compliance_score(framework)
            }
        
        return jsonify(matrix), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
