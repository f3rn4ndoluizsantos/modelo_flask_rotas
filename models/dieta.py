from database import db


class Dieta(db.Model):
    __tablename__ = "dieta"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(90), unique=True, nullable=False)
    descricao = db.Column(db.String(150), nullable=False)
    is_diet = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    data_hora_refeicao = db.Column(db.Date, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def get_id(self):
        return self.id

    def get_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "is_diet": self.is_diet,
            "data_hora_refeicao": self.data_hora_refeicao,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
