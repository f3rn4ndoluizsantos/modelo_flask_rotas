from flask_migrate import Migrate
from app import app
from database import db

migrate = Migrate(app, db)

# flask db init
# flask db migrate -m "Initial migration."
# flask db downgrade
