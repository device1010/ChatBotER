import os
import openai
import sys
from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders import PyPDFLoader


os.environ["OPENAI_API_KEY"] = "API-KEY"
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']


pages = []
for archivo in os.listdir("Resourcesp"):
    if archivo.endswith(".pdf"):
        
        ruta_pdf = os.path.join("Resourcesp", archivo)
        loader = PyPDFLoader(ruta_pdf)
        pages.append(loader.load())
        
        
#print(pages[0][1].page_content[0:100])
