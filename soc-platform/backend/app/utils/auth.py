from flask import request, jsonify
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User
from app import db

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            try:
                current_user_id = int(current_user_id)
            except Exception:
                pass
            current_user = User.query.get(current_user_id)
            if not current_user or not current_user.active:
                return jsonify({'error': 'User not found or inactive'}), 401
        except Exception as e:
            return jsonify({'error': 'Unauthorized', 'message': str(e)}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                try:
                    current_user_id = int(current_user_id)
                except Exception:
                    pass
                current_user = User.query.get(current_user_id)
                
                if not current_user or not current_user.active:
                    return jsonify({'error': 'User not found or inactive'}), 401
                
                if current_user.role not in roles:
                    return jsonify({'error': 'Insufficient permissions'}), 403
                    
            except Exception as e:
                return jsonify({'error': 'Unauthorized', 'message': str(e)}), 401
            
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

def log_audit(user, action, resource, resource_id=None, old_value=None, new_value=None, status='success'):
    from app.models import AuditLog
    try:
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        
        log = AuditLog(
            user_id=user.id if user else None,
            username=user.username if user else 'system',
            action=action,
            resource=resource,
            resource_id=resource_id,
            old_value=old_value,
            new_value=new_value,
            status=status,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging audit: {e}")
