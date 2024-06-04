from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, revision

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models

with app.app_context():
    revision(message="Add min_weight and max_weight to Offer", autogenerate=True)
    upgrade()
