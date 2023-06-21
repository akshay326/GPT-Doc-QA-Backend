from flask import jsonify
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

from andes import create_app
from andes.utils.wrappers import track_requests

# create app
app = create_app()

# simple test route
@app.route('/test', methods=['GET'])
@track_requests
def test():
    return jsonify({'message': 'success version 1'})

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# run server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
