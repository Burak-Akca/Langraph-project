import os
import bs4
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders.csv_loader import CSVLoader


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY bulunamadı! Lütfen çevre değişkenlerini kontrol edin.")

chat = GoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_key, temperature=0.4)





embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
# vector_store = .from_documents(documents=splits, embedding=embedding_model)
# retriever = vector_store.as_retriever()



def create_vector_database():
   print(os.getcwd())
   loader = CSVLoader(file_path="./langgraph/data/medquad.csv", source_column="question", encoding="utf-8")
   data=loader.load()
   vectorDB=FAISS.from_documents(documents=data,embedding=embedding_model)
   
   vectorDB.save_local("./langgraph/data/FAISS_DB")

   
def get_retriever():
    
   vectorDB=FAISS.load_local("./langgraph/data/FAISS_DB",embeddings=embedding_model,allow_dangerous_deserialization=True)
   retriever=vectorDB.as_retriever()
   return retriever

if __name__=="__main__":
    create_vector_database()