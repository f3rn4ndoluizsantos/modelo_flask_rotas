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
    data_hora_refeicao = data.get("data_hora_refeicao")

    dieta = Dieta(
        user_id=user_id,
        nome=nome,
        descricao=descricao,
        is_diet=is_diet,
        data_hora_refeicao=data_hora_refeicao,
    )
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


@main.route("/detail/<int:dieta_id>", methods=["GET"])
@login_required
def detail(dieta_id):
    try:
        dieta = db.session.execute(
            db.select(Dieta).filter(
                Dieta.id == dieta_id, Dieta.user_id == current_user.id
            )
        ).scalar_one()
        if not dieta:
            return jsonify({"message": "No row was found when one was required"}), 404
        return jsonify(dieta.get_dict())
    except Exception as e:
        print(e)
        return jsonify({"message": "Error when one was required"}), 500
