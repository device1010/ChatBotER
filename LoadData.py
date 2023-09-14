import os
import openai
import sys
from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter  import RecursiveCharacterTextSplitter, CharacterTextSplitter


def get_data_loaded():
    pages = ""
    for archivo in os.listdir("Resourcesp"):
        if archivo.endswith(".pdf"):
            ruta_pdf = os.path.join("Resourcesp", archivo)
            loader = PyPDFLoader(ruta_pdf)
            for page in loader.load():
                pages+=page.page_content
                #print(page.page_content)
            #pages.append(loader.load())

    return pages

def get_chunks(data,chunk_size,chunk_overlap):
    tr_splitter = RecursiveCharacterTextSplitter( chunk_size = chunk_size, chunk_overlap = chunk_overlap, length_function = len)
    chunks = tr_splitter.split_text(data)
    return chunks



os.environ["OPENAI_API_KEY"] = "API-KEY"
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']
 
data = get_data_loaded()
#print(data)
chunks = get_chunks(data,500,100)  #Send data, chunk size, chunk overlap, return chunks
print(chunks)
#print(pages[0][1].page_content[0:100])

