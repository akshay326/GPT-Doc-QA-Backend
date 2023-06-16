import uuid
from . import database as db

def generate_uuid():
    return str(uuid.uuid4())

#create a model for the database
class Document(db.Model):
    id = db.Column(db.String(), primary_key=True, default=generate_uuid)
    filename = db.Column(db.String(), nullable=False)
    page_count = db.Column(db.Integer, nullable=True)
    info = db.Column(db.JSON, default={})

    def __repr__(self):
        # include id and filename in the string representation
        return f'<Document {self.id}: {self.filename}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # add a method to return a dictionary representation of the object
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'page_count': self.page_count,
            'info': self.info
        }
