from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import openai
import sys
from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders import PyPDFLoader

os.environ["OPENAI_API_KEY"] = ""

loader = CSVLoader(file_path='fishfry-locations.csv', encoding="utf-8", csv_args={'delimiter': ','})

embeddings = OpenAIEmbeddings()
index_creator = VectorstoreIndexCreator()
docsearch = index_creator.from_loaders([loader])
chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.vectorstore.as_retriever(), input_key="question")