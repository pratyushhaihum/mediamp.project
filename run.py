from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.utils.db import db
from app.config import Config
from app.routes.auth_routes import auth_bp
from app.tasks import celery

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
CORS(app)
