from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Incident, User
from app.utils.auth import log_audit
from datetime import datetime

bp = Blueprint('incidents', __name__, url_prefix='/api/incidents')

@bp.route('', methods=['GET'])
@jwt_required()
def get_incidents():
    """Get all incidents"""
    try:
        severity = request.args.get('severity')
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = Incident.query
        
        if severity:
            query = query.filter_by(severity=severity)
        if status:
            query = query.filter_by(status=status)
        
        paginated = query.order_by(Incident.created_date.desc()).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'incidents': [i.to_dict() for i in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:incident_id>', methods=['GET'])
@jwt_required()
def get_incident(incident_id):
    """Get specific incident"""
    try:
        incident = Incident.query.get(incident_id)
        if not incident:
            return jsonify({'error': 'Incident not found'}), 404
        
        return jsonify(incident.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_incident():
    """Create new incident"""
    try:
        user_id = get_jwt_identity()
        try:
            user_id = int(user_id)
        except Exception:
            pass
        data = request.get_json()
        
        incident = Incident(
            incident_id=data.get('incident_id'),
            title=data.get('title'),
            description=data.get('description'),
            severity=data.get('severity', 'Medium'),
            status=data.get('status', 'open'),
            affected_systems=data.get('affected_systems'),
            impact=data.get('impact')
        )
        
        db.session.add(incident)
        db.session.commit()
        
        user = User.query.get(user_id)
        log_audit(user, 'INCIDENT_CREATED', 'Incident', incident.id, status='success')
        
        return jsonify({
            'message': 'Incident created',
            'incident': incident.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:incident_id>', methods=['PUT'])
@jwt_required()
def update_incident(incident_id):
    """Update incident"""
    try:
        user_id = get_jwt_identity()
        try:
            user_id = int(user_id)
        except Exception:
            pass
        incident = Incident.query.get(incident_id)
        
        if not incident:
            return jsonify({'error': 'Incident not found'}), 404
        
        data = request.get_json()
        
        if 'status' in data:
            incident.status = data['status']
        if 'root_cause' in data:
            incident.root_cause = data['root_cause']
        if 'assigned_to' in data:
            incident.assigned_to = data['assigned_to']
        if 'status' in data and data['status'] == 'resolved':
            incident.resolved_date = datetime.utcnow()
        
        db.session.commit()
        
        user = User.query.get(user_id)
        log_audit(user, 'INCIDENT_UPDATED', 'Incident', incident_id, status='success')
        
        return jsonify({
            'message': 'Incident updated',
            'incident': incident.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_incident_statistics():
    """Get incident statistics"""
    try:
        severities = {
            'Critical': Incident.query.filter_by(severity='Critical').count(),
            'High': Incident.query.filter_by(severity='High').count(),
            'Medium': Incident.query.filter_by(severity='Medium').count(),
            'Low': Incident.query.filter_by(severity='Low').count()
        }
        
        statuses = {
            'open': Incident.query.filter_by(status='open').count(),
            'investigating': Incident.query.filter_by(status='investigating').count(),
            'contained': Incident.query.filter_by(status='contained').count(),
            'resolved': Incident.query.filter_by(status='resolved').count()
        }
        
        avg_response_time = db.session.query(db.func.avg(Incident.response_time)).scalar() or 0
        
        return jsonify({
            'total': Incident.query.count(),
            'by_severity': severities,
            'by_status': statuses,
            'average_response_time': float(avg_response_time)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
