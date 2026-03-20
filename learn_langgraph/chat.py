from dotenv import load_dotenv
load_dotenv()
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

llm=init_chat_model(
    model="gemini-3-flash-preview",
    model_provider="google_genai"
)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    response= llm.invoke(state.get("messages"))
    return {"messages":["Hi, This is a message from chatbot node"]}


def sample_node(state:State):
    print("\n\nInside Sample Node")
    return {"messages":["sample Message Appender"]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("sample_node",sample_node)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","sample_node")
graph_builder.add_edge("sample_node",END)


graph=graph_builder.compile()

updated_state=graph.invoke(State({"messages":["what is my name ?"]}))
print("\n\nupdatd_state",updated_state)



#(start) --> chatbot --> sample_node --> (end)

#state = {"messages": ["Hi, My name is Harshendra"]}
#node runs : chatbot(state:["Hi, My name is Harshendra"]) --> returns {"messages":["Hi, This is a message from chatbot node"]}
#state = {"messages":["Hi, This is a message from chatbot node"]}
