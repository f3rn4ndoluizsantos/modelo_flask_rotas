from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from database import db
import bcrypt

auth = Blueprint("auth", __name__)


@auth.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data.get("email") or not data.get("password") or not data.get("user_name"):
        return jsonify({"message": "Email, UserName e senha sao obrigatorios"}), 400

    new_password = data.get("password").encode("utf-8")
    hashed = bcrypt.hashpw(new_password, bcrypt.gensalt())
    email = data.get("email")
    password = hashed
    user_name = data.get("user_name")
    user = User(email=email, password=password, user_name=user_name)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuário adicionado com sucesso!"}), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user_name = data.get("user_name")
    password = data.get("password")

    user = User.query.filter_by(user_name=user_name).first()

    if not user:
        return jsonify({"message": "Credenciais inválidas."}), 401

    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"message": "Credenciais inválidas."}), 401

    login_user(user)
    return jsonify({"message": "Login bem-sucedido!"})


@auth.route("/detail_user_logged", methods=["GET"])
@login_required
def detail_user_logged():
    user = db.session.get(User, current_user.id)
    return jsonify(user.get_dict()), 200


@auth.route("/logout")
@login_required
def logout():
    if not current_user.is_authenticated:
        return jsonify({"message": "Usuário não autenticado"}), 401

    logout_user()
    return jsonify({"message": "Logout bem-sucedido!"}), 200
    # flash("Você foi desconectado.", "success")
    # return redirect(url_for("auth.login"))
