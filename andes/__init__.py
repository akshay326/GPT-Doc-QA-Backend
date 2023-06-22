import time
import json
import logging
from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api
from andes.models import database as db
from andes.utils.config import UPLOAD_DIRECTORY, DB_PATH
from andes.routes.document import ns as document_ns

# set logging level
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Andes API', description='Andes API')

# register all namespaces for the API
api.add_namespace(document_ns)

# store files in uploads folder
app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY

# connect to a local database
app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
