from flask_login import UserMixin
from database import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
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
            "email": self.email,
            "user_name": self.user_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
