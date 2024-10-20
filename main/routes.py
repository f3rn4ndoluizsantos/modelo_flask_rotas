from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from models.dieta import Dieta
from database import db

main = Blueprint("main", __name__)


@main.route("/add", methods=["POST"])
@login_required
def add_dieta():
    if not current_user.is_authenticated:
        return jsonify({"message": "Usuário não autenticado"}), 401

    user_id = current_user.id

    data = request.get_json()
    nome = data.get("nome")
    descricao = data.get("descricao")
    is_diet = data.get("is_diet")

    dieta = Dieta(user_id=user_id, nome=nome, descricao=descricao, is_diet=is_diet)
    db.session.add(dieta)
    db.session.commit()

    return jsonify({"message": "Dieta adicionada com sucesso!"})


@main.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if not current_user.is_authenticated:
        return jsonify({"message": "Usuário não autenticado"}), 401

    user_id = current_user.id
    dietas = Dieta.query.filter_by(user_id=user_id).all()

    return jsonify({"dieta": [dieta.get_dict() for dieta in dietas]})
