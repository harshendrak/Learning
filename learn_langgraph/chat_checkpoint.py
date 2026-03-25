from dotenv import load_dotenv
load_dotenv()

from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from google import genai
from langgraph.checkpoint.mongodb import MongoDBSaver


llm=init_chat_model(
    model="gemini-3-flash-preview",
    model_provider="google_genai"
)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    response= llm.invoke(state.get("messages"))
    return {"messages":[response]}



graph_builder = StateGraph(State)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
    

   

DB_URI= "mongodb://admin:admin@localhost:27017"

with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer=compile_graph_with_checkpointer(checkpointer=checkpointer)

    config = {
            "configurable": {
                "thread_id": "Harshendra"
            }
        }

    upadated_state = None
 
    for chunk in graph_with_checkpointer.stream(
        {"messages":[input("input message")]},
        config,#type: ignore
        stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()
    
    
    





#(start) --> chatbot --> (end)

#state = {"messages": ["Hi, My name is Harshendra"]}
#node runs : chatbot(state:["Hi, My name is Harshendra"]) --> returns {"messages":["Hi, This is a message from chatbot node"]}
#state = {"messages":["Hi, This is a message from chatbot node"]}

# checkpointer will save the state after chatbot node execution in mongodb with thread_id as "Harshendra" and also save the edge which is executed in the graph.
