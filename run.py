import logging
from andes import create_app
from flask import jsonify

logging.getLogger().setLevel(logging.INFO)

# create app
app = create_app()

# simple test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'success version 1'})

# run server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
