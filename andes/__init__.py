import os
import time
import json
import logging
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from .models import database as db

# Load the .env file
load_dotenv()

# set logging level
logging.getLogger().setLevel(logging.INFO)

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
    
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    @app.after_request
    def log_request_info(response):
        # Calculate request duration to 3 decimal places
        request_duration = round(time.time() - request.start_time, 3)

        # Log the message
        message = {
            'message': 'API REQUEST',
            'client_address': request.remote_addr,
            'requested_url': request.url,
            'method': request.method,
            'path': request.path,
            'status': response.status,
            'duration': request_duration
        }
        logging.info(json.dumps(message))

        return response

    return app
