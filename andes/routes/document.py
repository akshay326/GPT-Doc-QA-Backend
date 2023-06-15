import os
from flask import request, jsonify, Blueprint
from werkzeug.utils import secure_filename
from pypdf import PdfReader
from andes.models import Document
from andes import UPLOAD_DIRECTORY

# create blueprints
document_blueprint = Blueprint('document', __name__)


@document_blueprint.route('/document/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_DIRECTORY, filename)
        file.save(filepath)

        reader = PdfReader(filepath)
        number_of_pages = len(reader.pages)

        # document = Document(name=filename, pages=number_of_pages)
        # document_service.add_document(document)

        return jsonify({'message': 'File has been uploaded and processed successfully'}), 200

    else:
        return jsonify({'error': 'Allowed file types are .pdf only'}), 400
