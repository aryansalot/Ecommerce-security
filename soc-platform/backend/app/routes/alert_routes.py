from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Alert, User
from app.utils.auth import log_audit
from datetime import datetime

bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

@bp.route('', methods=['GET'])
@jwt_required()
def get_alerts():
    """Get all alerts"""
    try:
        severity = request.args.get('severity')
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = Alert.query
        
        if severity:
            query = query.filter_by(severity=severity)
        if status:
            query = query.filter_by(status=status)
        
        paginated = query.order_by(Alert.created_date.desc()).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'alerts': [a.to_dict() for a in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:alert_id>', methods=['GET'])
@jwt_required()
def get_alert(alert_id):
    """Get specific alert"""
    try:
        alert = Alert.query.get(alert_id)
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        return jsonify(alert.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:alert_id>/acknowledge', methods=['PUT'])
@jwt_required()
def acknowledge_alert(alert_id):
    """Acknowledge alert"""
    try:
        user_id = get_jwt_identity()
        try:
            user_id = int(user_id)
        except Exception:
            pass
        alert = Alert.query.get(alert_id)
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        alert.status = 'acknowledged'
        alert.acknowledged_date = datetime.utcnow()
        alert.assigned_to = Alert.query.join(User).filter(User.id == user_id).scalar_one_or_none()
        
        db.session.commit()
        
        user = User.query.get(user_id)
        log_audit(user, 'ALERT_ACKNOWLEDGED', 'Alert', alert_id, status='success')
        
        return jsonify({
            'message': 'Alert acknowledged',
            'alert': alert.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:alert_id>/resolve', methods=['PUT'])
@jwt_required()
def resolve_alert(alert_id):
    """Resolve alert"""
    try:
        user_id = get_jwt_identity()
        try:
            user_id = int(user_id)
        except Exception:
            pass
        alert = Alert.query.get(alert_id)
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        alert.status = 'resolved'
        alert.resolved_date = datetime.utcnow()
        
        db.session.commit()
        
        user = User.query.get(user_id)
        log_audit(user, 'ALERT_RESOLVED', 'Alert', alert_id, status='success')
        
        return jsonify({
            'message': 'Alert resolved',
            'alert': alert.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_alert_statistics():
    """Get alert statistics"""
    try:
        severities = {
            'Critical': Alert.query.filter_by(severity='Critical').count(),
            'High': Alert.query.filter_by(severity='High').count(),
            'Medium': Alert.query.filter_by(severity='Medium').count(),
            'Low': Alert.query.filter_by(severity='Low').count(),
            'Info': Alert.query.filter_by(severity='Info').count()
        }
        
        statuses = {
            'new': Alert.query.filter_by(status='new').count(),
            'acknowledged': Alert.query.filter_by(status='acknowledged').count(),
            'in_progress': Alert.query.filter_by(status='in_progress').count(),
            'resolved': Alert.query.filter_by(status='resolved').count()
        }
        
        return jsonify({
            'total': Alert.query.count(),
            'by_severity': severities,
            'by_status': statuses
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
