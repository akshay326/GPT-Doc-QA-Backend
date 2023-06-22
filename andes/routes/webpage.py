from flask import request
from flask_restx import Resource, Namespace
from andes.services import webpage_service
from andes.services.auth import auth
from andes.utils.wrappers import track_requests
from andes.utils.slack import send_message
from andes.utils.config import SERVER_URL

ns = Namespace(
    'webpage', 
    path='/webpage',
    description='Webpage related operations'
)

@ns.route('')
class WebPage(Resource):
    @auth.login_required
    @track_requests
    def post(self):
        url = request.json['url']

        # create an empty webpage object in DB
        page = webpage_service.create_webpage(url)

        # enqueue the webpage for crawling
        webpage_service.enqueue_crawl(page)

        response = {
            'message': 'WebPage queued for crawling',
            'id': page.id,
            'url': f'{SERVER_URL}/webpage/{page.id}'
        }

        # send message to slack
        send_message(message=response, channel='#api-notifs')

        return response


@ns.route('/<string:id>')
class GetWebPage(Resource):
    @auth.login_required
    @track_requests
    def get(self, id):
        page = webpage_service.get_webpage(id)
        return page.to_dict()
    

@ns.route('/<string:id>/chat')
class WebPageChat(Resource):
    @auth.login_required
    @track_requests
    def get(self, id):
        page = webpage_service.get_webpage(id)
        chat_history = page.chat_history()
        return chat_history

    @auth.login_required
    @track_requests
    def post(self, id):
        # get message from request
        message = request.json['message']
        page = webpage_service.get_webpage(id)
        response = webpage_service.chat(page, message)

        # send message to slack
        send_message(
            message={
                'url': f'{SERVER_URL}/webpage/{page.id}',
                'message': message,
                'response': response
            }, 
            channel='#api-notifs'
        )

        return response
