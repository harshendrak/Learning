from dotenv import load_dotenv
from typing import TypedDict
from typing import Optional, Literal
from ollama import Client
from google import genai
from langgraph.graph import StateGraph, START, END

load_dotenv()
client=Client()

class State(TypedDict):
    user_query:str
    llm_output: Optional[str]
    is_good: Optional[bool]


def chatbot(state:State):
    print("In chatbot",state)
    response=client.chat(
        model="qwen3.5:397b-cloud",
        messages=[
            {"role":"user","content":state.get("user_query")}
        ]
    )

    state["llm_output"]=response.message.content
    return state


def evaluate_response(state:State) -> Literal["chatbot_gemini","endnode"]:
    print("In evaluate_response",state)
    if True:
        return "endnode"
    
    return "chatbot_gemini"


def chatbot_gemini(state:State):
    print("In chatbot_gemini",state)
    response=client.chat(
        model="qwen3.5:397b-cloud",
        messages=[
        {"role":"user","content":state.get("user_query")}])
    state["llm_output"]=response.message.content
    return state


def endnode(state:State):
    print("In endnode",state)
    return state





graph_builder=StateGraph(State)
 
graph_builder.add_node("chatbot",chatbot)
 
graph_builder.add_node("chatbot_gemini",chatbot_gemini)
 
graph_builder.add_node("endnode",endnode)


graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",evaluate_response)
graph_builder.add_edge("endnode",END)


graph=graph_builder.compile()
updated_state=graph.invoke(State({"user_query":"Hey, What is 2+2 ?"}))
print(updated_state)