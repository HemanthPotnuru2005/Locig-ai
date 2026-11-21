from langgraph.graph import START,END,StateGraph
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

llm = ChatGroq(model = "openai/gpt-oss-20b",temperature=0.7,max_tokens=2000)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]


def chat_node(state:ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

conn = sqlite3.connect(database = "data\chatbot.db",check_same_thread=False)

checkpointer = SqliteSaver(conn = conn)

graph = StateGraph(ChatState)

graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpointer.config["configurable"]['thread_id'])
        return list(all_threads)

































# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# from langchain_core.messages import SystemMessage,HumanMessage

# load_dotenv()

# llm = ChatGroq(model= 'openai/gpt-oss-20b',temperature= 0.7,max_tokens= 2000)


# def chat_llm(messages,system_message = "you are a helpfull Assistent"):
#     system_message = SystemMessage(system_message)
#     all_messages = [system_message,HumanMessage(content=messages)]
#     response = llm.invoke(all_messages)

#     return response.content