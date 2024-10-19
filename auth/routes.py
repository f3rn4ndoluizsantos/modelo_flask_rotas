from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User
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


# @auth.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form["email"]
#         password = request.form["password"]
#         user = User.query.filter_by(email=email).first()
#         if (
#             user and user.password == password
#         ):  # Aqui você deve usar hashing para senhas!
#             login_user(user)
#             flash("Login bem-sucedido!", "success")
#             return redirect(
#                 url_for("main.index")
#             )  # Redireciona para a página principal após login
#         else:
#             flash("Credenciais inválidas.", "danger")
#     return render_template("login.html")


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
    logout_user()
    flash("Você foi desconectado.", "success")
    return redirect(url_for("auth.login"))
