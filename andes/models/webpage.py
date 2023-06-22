import uuid
from typing import List
from andes import database as db

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


def generate_uuid():
    return str(uuid.uuid4())

#create a model for the database
class WebPage(db.Model):
    __tablename__ = 'webpage'

    id = db.Column(db.String(), primary_key=True, default=generate_uuid)
    url = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), default='')
    info = db.Column(db.JSON, default={})
    chats: Mapped[List["WebPageChatHistory"]] = relationship()

    def __repr__(self):
        # include id and filename in the string representation
        return f'<WebPage {self.id}: {self.url}>'
    
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
            'url': self.url,
            'title': self.title,
            'info': self.info,
            'chats': [chat.to_dict() for chat in self.chats]
        }
    
    # get chat history for a webpage
    def chat_history(self):
        return [chat.to_dict() for chat in self.chats]


# a model that stores the chat history of a webpage
class WebPageChatHistory(db.Model):
    __tablename__ = 'webpage_chat_history'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    webpage_id: Mapped[int] = mapped_column(ForeignKey("webpage.id"))
    question = db.Column(db.String(), nullable=False)
    answer = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __repr__(self):
        return f'<WebPageChatHistory {self.id}: {self.webpage.url}>'
    
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
            'created_at': str(self.created_at)
        }
