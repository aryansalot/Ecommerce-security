from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, decode_token
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///soc_platform.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt.init_app(app)

    # JWT error handlers and user lookup for better identity handling
    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        app.logger.error(f"Invalid JWT token: {reason}")
        app.logger.error(f"Authorization header on invalid token: {request.headers.get('Authorization')}")
        return jsonify({'error': 'Invalid token', 'message': reason}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        app.logger.error(f"Missing JWT: {reason}")
        app.logger.error(f"Authorization header on missing token: {request.headers.get('Authorization')}")
        return jsonify({'error': 'Missing token', 'message': reason}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        app.logger.error('Expired JWT token')
        return jsonify({'error': 'Token expired'}), 401

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data.get('sub') or jwt_data.get('identity')
        app.logger.debug(f"JWT user_lookup_callback identity: {identity}")
        try:
            user_id = int(identity)
        except Exception:
            user_id = identity
        from app.models import User
        return User.query.get(user_id)

    @app.before_request
    def debug_jwt_token():
        auth = request.headers.get('Authorization')
        if not auth:
            return
        app.logger.debug(f"Incoming Authorization header: {auth}")
        if auth.startswith('Bearer '):
            token = auth.split(' ', 1)[1]
            try:
                claims = decode_token(token)
                app.logger.debug(f"Decoded JWT claims: {claims}")
                identity = claims.get('sub') or claims.get('identity')
                app.logger.debug(f"Decoded JWT identity: {identity}")
            except Exception as e:
                app.logger.error(f"Error decoding JWT token: {type(e).__name__}: {e}")

    # Register blueprints
    from app.routes import auth_routes, dashboard_routes, vulnerability_routes
    from app.routes import incident_routes, threat_routes, alert_routes
    from app.routes import compliance_routes, mitre_routes, asset_routes, risk_routes
    
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(dashboard_routes.bp)
    app.register_blueprint(vulnerability_routes.bp)
    app.register_blueprint(incident_routes.bp)
    app.register_blueprint(threat_routes.bp)
    app.register_blueprint(alert_routes.bp)
    app.register_blueprint(compliance_routes.bp)
    app.register_blueprint(mitre_routes.bp)
    app.register_blueprint(asset_routes.bp)
    app.register_blueprint(risk_routes.bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Initialize sample data
        from app.utils.sample_data import initialize_sample_data
        initialize_sample_data()
    
    return app
