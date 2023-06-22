from flask import request, jsonify
from flask_restx import Resource, Namespace
from werkzeug.utils import secure_filename
from andes.services import document_service
from andes.services.auth import auth
from andes.utils.wrappers import track_requests
from andes.utils.slack import send_message
from andes.utils.config import SERVER_URL

ns = Namespace(
    'document', 
    path='/document',
    description='Document related operations'
)

@ns.route('')
class Document(Resource):
    @auth.login_required
    @track_requests
    def post(self):
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

            response = {
                'message': 'File has been uploaded successfully',
                'id': doc.id,
                'url': f'{SERVER_URL}/document/{doc.id}'
            }

            # send message to slack
            send_message(message=response, channel='#api-notifs')

            return response
        else:
            return {'error': 'Allowed file types are .pdf only'}


@ns.route('/<string:id>')
class GetDocument(Resource):
    @auth.login_required
    @track_requests
    def get(self, id):
        doc = document_service.get_document(id)
        return doc.to_dict()
    

@ns.route('/<string:id>/chat')
class DocumentChat(Resource):
    @auth.login_required
    @track_requests
    def get(self, id):
        doc = document_service.get_document(id)
        chat_history = doc.chat_history()
        return chat_history

    @auth.login_required
    @track_requests
    def post(self, id):
        # get message from request
        message = request.json['message']
        doc = document_service.get_document(id)
        response = document_service.chat(doc, message)

        # send message to slack
        send_message(
            message={
                'url': f'{SERVER_URL}/document/{doc.id}',
                'message': message,
                'response': response
            }, 
            channel='#api-notifs'
        )

        return response
