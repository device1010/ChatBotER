import os
import openai
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter  import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader
from langchain.schema.document import Document
from langchain.embeddings import OpenAIEmbeddings 
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from anzograph import Anzo
from SPARQLWrapper import JSON

def get_data_loaded():
    pages = ""
    for archivo in os.listdir("Resourcesp"):
        if archivo.endswith(".pdf"):
            ruta_pdf = os.path.join("Resourcesp", archivo)
            loader = PyPDFLoader(ruta_pdf)
            for page in loader.load():
                pages+=page.page_content
    return pages

def get_chunks(data,chunk_size,chunk_overlap):
    tr_splitter = RecursiveCharacterTextSplitter( chunk_size = chunk_size, chunk_overlap = chunk_overlap, length_function = len)
    chunks = tr_splitter.split_text(data)
    return chunks

def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    
    documents = []     #Changing format from str to langchain.schema.document.Document
    for text_chunk in text_chunks:
        doc = Document(page_content=text_chunk)
        documents.append(doc)

    vector_store = Chroma.from_documents(documents=documents, embedding= embeddings, persist_directory=db_directory)
    return vector_store

def  get_conversation_chain ( vector_store ): 
    conversation_chain = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), vector_store.as_retriever())
    return conversation_chain

def handler_user_input(question,conversation_chain,history):
    response = conversation_chain({"question": question, "chat_history":history})
    history.append((question,response["answer"]))
    return response["answer"]

def connection_gpt( prompt):
    messages = [{"role":"user","content": prompt}]
    res = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature = 0,
    )
    gptResponse = res.choices[0].message["content"]
    return gptResponse
    

def anzo_insert(prompt):
    if conection.connect():
            anzo_prompt = f"convierte el siguiente texto en un insert de SPARQL sin prefijos, para insertarlo a un grafo llamado Energias_Renovables: {prompt}"
            res = connection_gpt(anzo_prompt)
            print(res)
            conection.anzograph.method = 'POST'
            conection.anzograph.setQuery(f""" {res}""".encode("utf-8"))
            conection.anzograph.setReturnFormat(JSON)

            results = conection.anzograph.query().convert()

            if results in results:
                print( 'Prompt saved in graph')
            else:
                print('Error saving prompt in graph')


os.environ["OPENAI_API_KEY"] = "API-KEY"
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']
db_directory = './vectorizing' 

conection = Anzo()
anzo_connection = conection.connection

data = get_data_loaded()

chunks = get_chunks(data,500,100)  #Send data, chunk size, chunk overlap, return chunks

vector_store = get_vector_store(chunks)

conversation_chain = get_conversation_chain(vector_store)

history = []

#question = "que es biomasa?"
#response = handler_user_input(question,conversation_chain,history)
#print(response)

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt (BaseModel):
    user_prompt: str

@app.post('/chat_re')
async def Post_prompt (prompt: Prompt):
    response = handler_user_input (prompt.user_prompt,conversation_chain, history)
    anzo_insert(prompt)
    return {"response" : response }

