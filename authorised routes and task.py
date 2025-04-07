from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.utils.db import db
from app.tasks import long_running_task

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(name=data["name"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route("/auth/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email
    })

@auth_bp.route("/auth/start_task", methods=["POST"])
def start_task():
    data = request.get_json()
    task = long_running_task.apply_async(args=[data["duration"]])
    return jsonify({"task_id": task.id}), 202

@auth_bp.route("/auth/task_status/<task_id>", methods=["GET"])
def task_status(task_id):
    result = long_running_task.AsyncResult(task_id)
    return jsonify({"state": result.state, "result": result.result})


# app/tasks.py
from app.utils.celery import celery
import time

@celery.task
def long_running_task(duration):
    time.sleep(duration)
    return f"Task completed in {duration} seconds"

