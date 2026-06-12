from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Asset, User
from app.utils.auth import log_audit
from app.services.risk_service import RiskScoringEngine

bp = Blueprint('assets', __name__, url_prefix='/api/assets')

@bp.route('', methods=['GET'])
@jwt_required()
def get_assets():
    """Get all assets"""
    try:
        asset_type = request.args.get('asset_type')
        status = request.args.get('status')
        criticality = request.args.get('criticality')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = Asset.query
        
        if asset_type:
            query = query.filter_by(asset_type=asset_type)
        if status:
            query = query.filter_by(status=status)
        if criticality:
            query = query.filter_by(criticality=criticality)
        
        paginated = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'assets': [a.to_dict() for a in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:asset_id>', methods=['GET'])
@jwt_required()
def get_asset(asset_id):
    """Get specific asset"""
    try:
        asset = Asset.query.get(asset_id)
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        asset_data = asset.to_dict()
        asset_data['risk_score'] = RiskScoringEngine.calculate_asset_risk_score(asset)
        
        return jsonify(asset_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_asset():
    """Create new asset"""
    try:
        user_id = get_jwt_identity()
        try:
            user_id = int(user_id)
        except Exception:
            pass
        data = request.get_json()
        
        asset = Asset(
            asset_id=data.get('asset_id'),
            asset_name=data.get('asset_name'),
            asset_type=data.get('asset_type'),
            ip_address=data.get('ip_address'),
            hostname=data.get('hostname'),
            os=data.get('os'),
            criticality=data.get('criticality', 'Medium'),
            owner=data.get('owner')
        )
        
        db.session.add(asset)
        db.session.commit()
        
        user = User.query.get(user_id)
        log_audit(user, 'ASSET_CREATED', 'Asset', asset.id, status='success')
        
        return jsonify({
            'message': 'Asset created',
            'asset': asset.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:asset_id>', methods=['PUT'])
@jwt_required()
def update_asset(asset_id):
    """Update asset"""
    try:
        user_id = get_jwt_identity()
        try:
            user_id = int(user_id)
        except Exception:
            pass
        asset = Asset.query.get(asset_id)
        
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        
        data = request.get_json()
        
        if 'status' in data:
            asset.status = data['status']
        if 'criticality' in data:
            asset.criticality = data['criticality']
        if 'owner' in data:
            asset.owner = data['owner']
        if 'vulnerabilities' in data:
            asset.vulnerabilities = data['vulnerabilities']
        
        db.session.commit()
        
        user = User.query.get(user_id)
        log_audit(user, 'ASSET_UPDATED', 'Asset', asset_id, status='success')
        
        return jsonify({
            'message': 'Asset updated',
            'asset': asset.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_asset_statistics():
    """Get asset statistics"""
    try:
        by_type = {}
        types = ['server', 'database', 'application', 'endpoint']
        
        for atype in types:
            by_type[atype] = Asset.query.filter_by(asset_type=atype).count()
        
        by_criticality = {
            'Critical': Asset.query.filter_by(criticality='Critical').count(),
            'High': Asset.query.filter_by(criticality='High').count(),
            'Medium': Asset.query.filter_by(criticality='Medium').count(),
            'Low': Asset.query.filter_by(criticality='Low').count()
        }
        
        return jsonify({
            'total': Asset.query.count(),
            'active': Asset.query.filter_by(status='active').count(),
            'by_type': by_type,
            'by_criticality': by_criticality
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
