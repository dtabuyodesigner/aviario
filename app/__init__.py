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

    @app.route('/api/v2/ping')
    def ping():
        return {'status': 'ok', 'message': 'AVIARIO Web API v2 is running'}

    return app
