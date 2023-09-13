# Contains all prompts used in the project.
import os

# get current directory
CURRENT_DIR = os.path.dirname(__file__)

FIN_QA_PROMPT = open(os.path.join(CURRENT_DIR, 'FIN_QA_PROMPT.txt')).read()