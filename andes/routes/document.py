from flask import request, jsonify, Blueprint
from werkzeug.utils import secure_filename
from andes.services import document_service

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

        # create an empty document object in DB
        doc = document_service.create_document(filename)

        # save the file to the uploads folder
        document_service.save_file(doc, file)

        return jsonify({
            'message': 'File has been uploaded successfully',
            'endpoint': f'/document/{doc.id}'
        }), 200
    else:
        return jsonify({'error': 'Allowed file types are .pdf only'}), 400