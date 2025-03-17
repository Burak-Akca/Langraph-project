import os
from typing import Literal, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
import importlib.util
import os
import sys

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_directory)
from langgraph.ingestion import get_retriever

# Çevre değişkenlerini yükle
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY bulunamadı! Lütfen çevre değişkenlerini kontrol edin.")

# LLM başlatma
llm = ChatMistralAI(model="mistral-large-latest", temperature=0)

# Yapılandırılmış çıktı modeli
class GradeDocuments(BaseModel):
    binaryscore: str  = Field(
        ...
    )
    

# Modeli yapılandırılmış çıktı ile kullan
structured_llm_grader = llm.with_structured_output(GradeDocuments)

# Sistem mesajı tanımlama
system_prompt = """
You are a grader assessing whether an LLM generation is grounded in /
 supported by a set of retrieved facts. \n Give a binary score 'yes' or 'no'.
   'Yes' means that the answer is grounded in / supported by the set of facts.
"""

# Prompt şablonu oluşturma
grade_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Retrieved document: {document} User question: {question}")
])

# Router pipeline
retrival_grader=grade_prompt |  structured_llm_grader



retriever=get_retriever()




# Test çağrısı
if __name__ == "__main__":
      user_question="quantum physics5?"
      docs=retriever.get_relevant_documents(user_question)
      retrieved_document=docs[0].page_content
      print(retrieved_document)
      print(retrival_grader.invoke({
           "question":user_question,"document":retrieved_document


      }))
