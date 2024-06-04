from flask import Flask
from config import Config
from models import db, migrate
from routes import register_blueprints

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)

register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)
