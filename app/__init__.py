from flask import Flask
from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    
    from app.api.birds import bp as birds_bp
    app.register_blueprint(birds_bp, url_prefix='/api/v2/birds')
    
    from app.api.genetics import bp as genetics_bp
    app.register_blueprint(genetics_bp, url_prefix='/api/v2/genetics')

    from app.api.breeding import bp as breeding_bp
    app.register_blueprint(breeding_bp, url_prefix='/api/v2/breeding')

    from app.api.health import bp as health_bp
    app.register_blueprint(health_bp, url_prefix='/api/v2/health')



    # Frontend Integration
    import os
    from flask import send_from_directory

    # Parent directory (AVIARIO root)
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    @app.route('/')
    def index():
        return send_from_directory(PROJECT_ROOT, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(PROJECT_ROOT, path)

    @app.route('/api/v2/ping')
    def ping():
        return {'status': 'ok', 'message': 'AVIARIO Web API v2 is running'}

    return app
