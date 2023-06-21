import os
from flask import request, jsonify, Blueprint
from werkzeug.utils import secure_filename
from andes.services import document_service
from andes.services.auth import auth
from andes.utils.wrappers import track_requests

SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:8000')
# create blueprints
document_blueprint = Blueprint('document', __name__)


@document_blueprint.route('/document/upload', methods=['POST'])
@auth.login_required
@track_requests
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)

        # create an empty document object in DB
        doc = document_service.create_document(filename)

        # save the file to the uploads folder
        document_service.save_file(doc, file)

        # create a langchain index for the document
        document_service.enqueue_index_gen(doc)

        return jsonify({
            'message': 'File has been uploaded successfully',
            'id': doc.id,
            'url': f'{SERVER_URL}/document/{doc.id}'
        }), 200
    else:
        return jsonify({'error': 'Allowed file types are .pdf only'}), 400


@document_blueprint.route('/document/<id>', methods=['GET'])
@auth.login_required
@track_requests
def get_document(id):
    doc = document_service.get_document(id)
    return jsonify(doc.to_dict()), 200


@document_blueprint.route('/document/<id>/chat_history', methods=['GET'])
@auth.login_required
@track_requests
def document_chat_history(id):
    doc = document_service.get_document(id)
    chat_history = doc.chat_history()
    return jsonify(chat_history), 200


@document_blueprint.route('/document/<id>/chat', methods=['POST'])
@auth.login_required
@track_requests
def document_chat(id):
    # get message from request
    message = request.json['message']
    doc = document_service.get_document(id)
    response = document_service.chat(doc, message)
    return jsonify(response), 200
