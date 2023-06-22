import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

UPLOAD_DIRECTORY = os.getenv('UPLOAD_DIRECTORY')
DB_PATH = os.getenv('DB_PATH')
SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:8000')