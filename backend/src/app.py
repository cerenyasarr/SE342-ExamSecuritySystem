from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.config import config
from src.models import db

# Import blueprints
from src.routes.auth_routes import auth_bp
from src.routes.user_routes import user_bp
from src.routes.room_routes import room_bp
from src.routes.exam_routes import exam_bp
from src.routes.student_exam_routes import student_exam_bp
from src.routes.violation_routes import violation_bp


def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=['*'])
    JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(room_bp, url_prefix='/api/rooms')
    app.register_blueprint(exam_bp, url_prefix='/api/exams')
    app.register_blueprint(student_exam_bp, url_prefix='/api/student-exams')
    app.register_blueprint(violation_bp, url_prefix='/api/violations')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Exam Security API is running'}
    
    # Root endpoint - API info
    @app.route('/')
    def api_info():
        return {
            'name': 'Exam Security API',
            'version': '1.0',
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth',
                'users': '/api/users',
                'rooms': '/api/rooms',
                'exams': '/api/exams',
                'student-exams': '/api/student-exams',
                'violations': '/api/violations'
            }
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app


# Create app instance for Flask CLI
app = create_app()
