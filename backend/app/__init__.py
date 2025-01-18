from flask import Flask
from flask_cors import CORS
from ..config.config import config
from .routes.auth_routes import auth_bp
from .routes.event_routes import events_bp
from .routes.user_routes import users_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    CORS(app)
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(events_bp, url_prefix='/api/events')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    return app
