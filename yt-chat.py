from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
load_dotenv()


# Indexing

video_id="Gfr50f6ZBvo"

try:
    ytt_api = YouTubeTranscriptApi()
    fetched = ytt_api.fetch(video_id, languages=['en'])
    transcript = " ".join([chunk.text for chunk in fetched])
    print(transcript[:500])

except TranscriptsDisabled:
    print("No captions available")


splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,

)
chunks=splitter.create_documents([transcript])

# vector store 

embedding_model=OllamaEmbeddings(
    model="qwen3-embedding:0.6b",base_url="http://localhost:11434"
)

vector_store=FAISS.from_documents(chunks,embedding_model)


retriever=vector_store.as_retriever(search_type="similarity",search_kwargs={"k":4})


# Augmention 


llm=GoogleGenerativeAI(model="gemma-4-31b-it", temperature=0.2)

prompt=PromptTemplate(
template="""
You are a helpful assistant.
Answer only from the provided transcript context.
If the context is insufficient just say you don't know.
{context}
Question:{question}
""",
input_variables=['context','question']
)



question="is the topic of aliens discussed in this video? if yes then what was disscussed"
retrieved_docs=retriever.invoke(question)

context_text="\n\n".join(doc.page_content for doc in retrieved_docs )

final_prompt=prompt.invoke({"context":context_text,"question":question})

# generation

answer=llm.invoke(final_prompt)
print(answer)

