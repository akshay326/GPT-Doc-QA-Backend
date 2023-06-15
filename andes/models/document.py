from sqlalchemy_utils import UUIDType
import uuid
from . import database as db


#create a model for the database
class Document(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    filename = db.Column(db.String(50), nullable=False)
    index_path = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        # include id and filename in the string representation
        return f'<Document {self.id}: {self.filename}>'
