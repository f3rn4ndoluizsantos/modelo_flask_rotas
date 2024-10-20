from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import User
from database import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SECRET_KEY"] = "s3cr3t"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:admin123@127.0.0.1:3306/flask-diet"
)

login_manager = LoginManager(app)
db.init_app(app)
login_manager.login_view = "auth.login"  # Define a rota de login

migrate = Migrate(app, db)

from auth.routes import auth as auth_blueprint
from main.routes import main as main_blueprint

app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(main_blueprint, url_prefix="/dieta")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)
