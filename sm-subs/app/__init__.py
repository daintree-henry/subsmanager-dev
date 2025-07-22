import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS 허용 도메인을 환경 변수에서 가져오기
    allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173').split(',')

    # CORS 적용
    CORS(app, resources={r"/*": {"origins": allowed_origins}}, supports_credentials=True)

    db.init_app(app)
    jwt.init_app(app)

    # Logger 설정
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)   
    if not app.logger.handlers:
        app.logger.addHandler(handler)

    # 로깅 레벨 설정
    app.logger.setLevel(logging.INFO)
    app.logger.info("Flask application started")
    app.logger.propagate = False   

    from app.routes import bp as api_bp
    CORS(api_bp)
    app.register_blueprint(api_bp)

    return app
