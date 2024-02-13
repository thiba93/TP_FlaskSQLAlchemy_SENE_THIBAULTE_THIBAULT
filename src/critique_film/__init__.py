from flask import Flask
from flask_migrate import Migrate
from .models import Utilisateur
from .database import db 

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@<domaine|ip>:<port>/<database>'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@db/critiques_de_films'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    return app


