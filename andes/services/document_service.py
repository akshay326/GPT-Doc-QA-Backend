import os
from andes.models import Document
from andes import UPLOAD_DIRECTORY


def create_document(filename: str):
    """
    create Document sqlalchemy model object
    """
    doc = Document(filename=filename)
    doc.save()
    return doc


def save_file(doc: Document, file):
    """
    saves the file to the uploads folder
    """
    print(doc.id, doc.filename)
    filepath = os.path.join(UPLOAD_DIRECTORY, doc.id, doc.filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file.save(filepath)
    return filepath
