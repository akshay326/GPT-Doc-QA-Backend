import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .models import database as db

# Load the .env file
load_dotenv()

UPLOAD_DIRECTORY = os.getenv('UPLOAD_DIRECTORY')
DB_PATH = os.getenv('DB_PATH')

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
