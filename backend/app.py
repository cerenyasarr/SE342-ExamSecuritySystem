from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import db

# Import blueprints
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.room_routes import room_bp
from routes.course_routes import course_bp
from routes.exam_routes import exam_bp
from routes.student_exam_routes import student_exam_bp
from routes.violation_routes import violation_bp


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
    app.register_blueprint(course_bp, url_prefix='/api/courses')
    app.register_blueprint(exam_bp, url_prefix='/api/exams')
    app.register_blueprint(student_exam_bp, url_prefix='/api/student-exams')
    app.register_blueprint(violation_bp, url_prefix='/api/violations')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Exam Security API is running'}
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
