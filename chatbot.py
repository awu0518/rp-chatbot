from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import InferenceClient
from langchain_pinecone import PineconeVectorStore
import gradio as gr
import os
from dotenv import load_dotenv

from functions import *

load_dotenv(".env")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
huggingface_api_key = os.environ.get("HUGGINGFACE_API_KEY")

pc = Pinecone(api_key=pinecone_api_key)

index_name = "renegade-platinum"

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = PineconeVectorStore(index=index, embedding=embeddings)
client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.3",
    token=huggingface_api_key,
)

def chat(message, history):
    documents = vector_store.similarity_search(message, k=10)
    context = ""

    for doc in documents:
        context += doc.page_content + "\n"

    query = f"""
    Answer the following question about Pokemon Renegade Platinum with the help of the given context:

    Context: {context}
    Question: {message}
    """
    
    response = ""
    for message in client.chat_completion(
        messages=[{"role": "user", "content": query}],
        max_tokens=1000,
        stream=True,
    ):
        response += message.choices[0].delta.content if message.choices[0].delta.content is not None else ""
    return response

gr.ChatInterface(fn=chat).launch()



