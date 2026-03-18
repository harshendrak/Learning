from google import genai
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore


gemini_client = genai.Client()
# Vector embedding model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001" 
)


vector_db=QdrantVectorStore.from_existing_collection(

    embedding=embedding_model, 
    url="http://localhost:6333",
    collection_name="Learning RAG"
)


def process_query(query):
    print("Searching Chunks",query)
    search_results=vector_db.similarity_search(query=query)

    context="\n\n\n".join([f"Page Content: {result.page_content}\nPage Number:{result.metadata['page_label']}\nFile Location : {result.metadata['source']}" for result in search_results])

    SYSTEM_PROMPT= f"""
    You are a helpful AI assistant whoa answers user queries based on the available 
    context from a PDF file along with the page_contents and page numbers.

    You should only answer the user based on the following context and navigate the
    user to open the right page number to know more.

    Context:
    {context}
    
    """


    
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query,
        config={"system_instruction": SYSTEM_PROMPT}   # Fix 2: correct way to pass system prompt
    )


    print(f"{response.text}")
    return response.text