from dotenv import load_dotenv
from google import genai
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from langchain_qdrant import QdrantVectorStore

load_dotenv()



pdf_path=Path(__file__).parent/"cheese.pdf"

# load this file in python program
loader=PyPDFLoader(file_path=pdf_path)
docs=loader.load()

# Chunking the document into smaller pieces for better processing and embedding

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)
chunks=text_splitter.split_documents(documents=docs)

# vector embedding using Google's embedding model
embedding_model=GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001")

vector_db=QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="Book"
)

print("Indexing of documents done ....")