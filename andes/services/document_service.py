import os
import logging
from pypdf import PdfReader
from rq import Retry

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.openai import OpenAIEmbeddings

from andes.models import Document, DocumentChatHistory
from andes.utils.config import UPLOAD_DIRECTORY
from andes.services.serialization import pickle_dump, pickle_load
from andes.services.rq import QUEUES


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
    logging.info(f"Saving Document {doc}")
    filepath = os.path.join(UPLOAD_DIRECTORY, doc.id, doc.filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file.save(filepath)
    return filepath


def get_document(id: str):
    """
    get Document sqlalchemy model object
    """
    doc = Document.query.get(id)
    return doc


def _split_pdf(fpath: str, chunk_size=4000, chunk_overlap=50) -> list[str]:
    """
    Pre-process PDF into chunks
    """
    reader = PdfReader(fpath)
    raw_document_text = '\n\n'.join([page.extract_text() for page in reader.pages])

    # split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap  = chunk_overlap,
        length_function = len,
        add_start_index = True,
    )

    splits = text_splitter.create_documents([raw_document_text])
    texts = [split.page_content for split in splits]
    return texts


def create_index(doc: Document):
    """
    create a langchain index for the document
    """
    logging.info(f"Started creating index for {doc.filename}")

    filepath = os.path.join(UPLOAD_DIRECTORY, doc.id, doc.filename)
    doc_splits = _split_pdf(filepath)

    # create a langchain index for each chunk
    logging.info(f"Building index for {doc.filename}")
    embeddings = OpenAIEmbeddings()
    index = FAISS.from_texts(doc_splits, embeddings)

    # save the index to disk
    index_path = os.path.join(UPLOAD_DIRECTORY, doc.id, 'index.pkl')
    pickle_dump(index, index_path)


def enqueue_index_gen(doc: Document):
    """
    enqueue the index generation task into a redis queue
    """
    QUEUES['index_gen'].enqueue(create_index, doc, retry=Retry(max=3))
    logging.info(f"Enqueued index generation for {doc.filename}")


def chat(doc: Document, message: str) -> str:
    # query openai on the langchain index

    # sanity checks
    if not os.path.exists(os.path.join(UPLOAD_DIRECTORY, doc.id, 'index.pkl')):
        raise ValueError("Index does not exist for this document")
    
    assert message is not None, "Message cannot be empty"

    # load the index from disk
    index_path = os.path.join(UPLOAD_DIRECTORY, doc.id, 'index.pkl')
    index = pickle_load(index_path)

    # load the chat history from document
    chat_history = doc.chat_history()

    # format the history
    chat_history = [
        (
        chat['question'],
        chat['answer']
        ) for chat in chat_history
    ]

    qa = ConversationalRetrievalChain.from_llm(
        OpenAI(temperature=0), 
        index.as_retriever()
    )
    response = qa({
        "question": message, 
        "chat_history": chat_history
    })

    # save the chat history
    DocumentChatHistory(
        document_id = doc.id,
        question = message,
        answer = response['answer']
    ).save()

    return response['answer']
