from flask import Flask, request
from flask_cors import CORS
from config.config import config
from .routes.auth_routes import auth_bp
from .routes.event_routes import events_bp
from .routes.user_routes import users_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, 
         resources={r"/api/*": {"origins": "http://localhost:3000"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(events_bp, url_prefix='/api/events')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    # Global OPTIONS handler
    @app.route('/api/auth/login', methods=['OPTIONS'])
    @app.route('/api/auth/register', methods=['OPTIONS'])
    def handle_auth_options():
        response = app.make_default_options_response()
        return response

    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    return app
