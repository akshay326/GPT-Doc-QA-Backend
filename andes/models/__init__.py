from flask_sqlalchemy import SQLAlchemy

# initialize database
database = SQLAlchemy()

# import models
from .document import Document, DocumentChatHistory
