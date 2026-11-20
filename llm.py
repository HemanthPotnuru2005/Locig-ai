from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage,HumanMessage

load_dotenv()

llm = ChatGroq(model= 'openai/gpt-oss-20b',temperature= 0.7,max_tokens= 2000)


def chat_llm(messages,system_message = "you are a helpfull Assistent"):
    system_message = SystemMessage(system_message)
    all_messages = [system_message,HumanMessage(content=messages)]
    response = llm.invoke(all_messages)

    return response.content
