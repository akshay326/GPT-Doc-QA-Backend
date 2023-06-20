import os
from flask_httpauth import HTTPTokenAuth
from andes.services.serialization import json_load

# Define your API keys here
API_KEYS = json_load(os.getenv('PATH_TO_API_KEYS', None))

auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(api_key):
    if api_key in API_KEYS:
        return True
    return False
