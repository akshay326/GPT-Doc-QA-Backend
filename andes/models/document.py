import uuid
from typing import List
from . import database as db

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


def generate_uuid():
    return str(uuid.uuid4())

#create a model for the database
class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.String(), primary_key=True, default=generate_uuid)
    filename = db.Column(db.String(), nullable=False)
    page_count = db.Column(db.Integer, nullable=True)
    info = db.Column(db.JSON, default={})
    chats: Mapped[List["DocumentChatHistory"]] = relationship()

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
    
    # get chat history for a document
    def chat_history(self):
        return [chat.to_dict() for chat in self.chats]



# a model that stores the chat history of a document
class DocumentChatHistory(db.Model):
    __tablename__ = 'document_chat_history'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("document.id"))
    question = db.Column(db.String(), nullable=False)
    answer = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __repr__(self):
        return f'<DocumentChatHistory {self.id}: {self.document.filename}>'
    
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
            'question': self.question,
            'answer': self.answer,
            'created_at': self.created_at
        }
    
