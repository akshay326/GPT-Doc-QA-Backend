import time
import json
import logging
from andes import create_app
from flask import jsonify, request

logging.getLogger().setLevel(logging.INFO)

# create app
app = create_app()

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request_info(response):
    # Calculate request duration to 3 decimal places
    request_duration = round(time.time() - request.start_time, 3)
    
    # Get request details
    method = request.method
    path = request.path
    status = response.status

    # Log the message
    message = {
        'message': 'API REQUEST',
        'method': method,
        'path': path,
        'status': status,
        'duration': request_duration
    }
    logging.info(json.dumps(message))

    return response

# simple test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'success version 1'})

# run server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
