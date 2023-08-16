from flask import request, jsonify, Response
from flask_restx import Resource, Namespace
from werkzeug.utils import secure_filename
from andes.services import document_service
from andes.services.auth import auth
from andes.utils.wrappers import track_requests
from andes.utils.slack import send_message
from andes.utils.config import SERVER_URL
from andes.schemas.extraction_config import ExtractionConfigSchema

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
            return Response(status=400, response='No file part in the request')

        file = request.files['file']

        if file.filename == '':
            return Response(status=400, response='No file selected for uploading')

        filename = secure_filename(file.filename)

        try:
            # create an empty document object in DB
            doc = document_service.create_document(filename)
        except Exception as e:
            return Response(status=400, response=str(e))

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
        answer = document_service.chat(doc, message)

        # send message to slack
        send_message(
            message={
                'action': 'chat',
                'url': f'{SERVER_URL}/document/{doc.id}',
                'question': message,
                'answer': answer
            }, 
            channel='#api-notifs'
        )

        return answer


@ns.route('/<string:id>/extract')
class DocumentExtract(Resource):
    @auth.login_required
    @track_requests
    def post(self, id):
        # validate extraction config as request json
        try:
            ExtractionConfigSchema.validate(request.json)
            config = request.json
            doc = document_service.get_document(id)
            response = document_service.extract(doc, config)
            return response
        except Exception as e:
            return Response(status=400, response=str(e))
