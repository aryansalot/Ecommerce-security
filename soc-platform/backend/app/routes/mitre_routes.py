from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import MitreAttack
from sqlalchemy import func

bp = Blueprint('mitre', __name__, url_prefix='/api/mitre')

@bp.route('/techniques', methods=['GET'])
@jwt_required()
def get_techniques():
    """Get all MITRE ATT&CK techniques"""
    try:
        tactic = request.args.get('tactic')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = MitreAttack.query
        
        if tactic:
            query = query.filter_by(tactic=tactic)
        
        paginated = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'techniques': [t.to_dict() for t in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tactics', methods=['GET'])
@jwt_required()
def get_tactics():
    """Get all tactics"""
    try:
        tactics = db.session.query(MitreAttack.tactic).distinct().all()
        return jsonify([t[0] for t in tactics]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/matrix', methods=['GET'])
@jwt_required()
def get_attack_matrix():
    """Get MITRE ATT&CK matrix"""
    try:
        from app import db
        
        tactics = [row[0] for row in db.session.query(MitreAttack.tactic).distinct().all()]
        matrix = {}
        
        for tactic in tactics:
            techniques = MitreAttack.query.filter_by(tactic=tactic).all()
            matrix[tactic] = {
                'count': len(techniques),
                'detected': sum(1 for t in techniques if t.detection_count > 0),
                'techniques': [t.to_dict() for t in techniques]
            }
        
        return jsonify(matrix), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/detections', methods=['GET'])
@jwt_required()
def get_detections():
    """Get detection statistics"""
    try:
        from app import db
        
        total_techniques = MitreAttack.query.count()
        detected_techniques = MitreAttack.query.filter(MitreAttack.detection_count > 0).count()
        
        return jsonify({
            'total_techniques': total_techniques,
            'detected_techniques': detected_techniques,
            'detection_rate': (detected_techniques / total_techniques * 100) if total_techniques > 0 else 0
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
