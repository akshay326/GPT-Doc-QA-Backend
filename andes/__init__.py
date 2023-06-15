from flask import Flask, jsonify
from flask_cors import CORS
from .config import UPLOAD_DIRECTORY, DB_PATH
from .models import database as db

# init app
def create_app():
    app = Flask(__name__)
    CORS(app)

    # store files in uploads folder
    app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY

    # connect to a local database
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # register blueprints
    from .routes.document import document_blueprint
    app.register_blueprint(document_blueprint)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app
