# import warnings

# warnings.filterwarnings("ignore", category=UserWarning)

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI


pdf_path = Path(__file__).parent / "cheese.pdf"

# load this file in python program
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# chunking the document into smaller pieces for better processing and embedding
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400 # helps to maintain context between chunks by overlapping them
)

chunks=text_splitter.split_documents(documents=docs)


# vector embeddings using OpenAI's embedding model

embedding_model= OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_store= QdrantVectorStore.from_documents(

    documents=chunks,
    emdedding=embedding_model,
    url="http://localhost:6333",
    collection_name="Learning RAG"


)


print("Indexing of documents done ....")