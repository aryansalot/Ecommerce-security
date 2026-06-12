from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Threat, User
from app.utils.auth import log_audit

bp = Blueprint('threats', __name__, url_prefix='/api/threats')

@bp.route('', methods=['GET'])
@jwt_required()
def get_threats():
    """Get all threats"""
    try:
        threat_type = request.args.get('threat_type')
        ioc_type = request.args.get('ioc_type')
        severity = request.args.get('severity')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = Threat.query
        
        if threat_type:
            query = query.filter_by(threat_type=threat_type)
        if ioc_type:
            query = query.filter_by(ioc_type=ioc_type)
        if severity:
            query = query.filter_by(severity=severity)
        
        paginated = query.order_by(Threat.detected_date.desc()).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'threats': [t.to_dict() for t in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:threat_id>', methods=['GET'])
@jwt_required()
def get_threat(threat_id):
    """Get specific threat"""
    try:
        threat = Threat.query.get(threat_id)
        if not threat:
            return jsonify({'error': 'Threat not found'}), 404
        
        return jsonify(threat.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_threat():
    """Create new threat intelligence"""
    try:
        user_id = get_jwt_identity()
        try:
            user_id = int(user_id)
        except Exception:
            pass
        data = request.get_json()
        
        threat = Threat(
            threat_id=data.get('threat_id'),
            threat_name=data.get('threat_name'),
            threat_type=data.get('threat_type'),
            ioc_type=data.get('ioc_type'),
            ioc_value=data.get('ioc_value'),
            severity=data.get('severity', 'Medium'),
            source=data.get('source'),
            description=data.get('description'),
            confidence=data.get('confidence', 75)
        )
        
        db.session.add(threat)
        db.session.commit()
        
        user = User.query.get(user_id)
        log_audit(user, 'THREAT_CREATED', 'Threat', threat.id, status='success')
        
        return jsonify({
            'message': 'Threat created',
            'threat': threat.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:threat_id>', methods=['PUT'])
@jwt_required()
def update_threat(threat_id):
    """Update threat"""
    try:
        user_id = get_jwt_identity()
        try:
            user_id = int(user_id)
        except Exception:
            pass
        threat = Threat.query.get(threat_id)
        
        if not threat:
            return jsonify({'error': 'Threat not found'}), 404
        
        data = request.get_json()
        
        if 'status' in data:
            threat.status = data['status']
        if 'confidence' in data:
            threat.confidence = data['confidence']
        if 'description' in data:
            threat.description = data['description']
        
        db.session.commit()
        
        user = User.query.get(user_id)
        log_audit(user, 'THREAT_UPDATED', 'Threat', threat_id, status='success')
        
        return jsonify({
            'message': 'Threat updated',
            'threat': threat.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/iocs', methods=['GET'])
@jwt_required()
def get_iocs():
    """Get IOC statistics"""
    try:
        ioc_breakdown = {}
        ioc_types = ['ip', 'domain', 'hash', 'email', 'file', 'url']
        
        for ioc_type in ioc_types:
            ioc_breakdown[ioc_type] = Threat.query.filter_by(ioc_type=ioc_type).count()
        
        return jsonify(ioc_breakdown), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_threat_statistics():
    """Get threat statistics"""
    try:
        by_type = {}
        types = ['malware', 'ransomware', 'APT', 'botnet', 'phishing']
        
        for ttype in types:
            by_type[ttype] = Threat.query.filter_by(threat_type=ttype).count()
        
        severities = {
            'Critical': Threat.query.filter_by(severity='Critical').count(),
            'High': Threat.query.filter_by(severity='High').count(),
            'Medium': Threat.query.filter_by(severity='Medium').count(),
            'Low': Threat.query.filter_by(severity='Low').count()
        }
        
        return jsonify({
            'total': Threat.query.count(),
            'active': Threat.query.filter_by(status='active').count(),
            'by_type': by_type,
            'by_severity': severities
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
