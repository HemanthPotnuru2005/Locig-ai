from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from llm import chat_llm

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-001")


#takes the doc as input and convert them into text and give it back 
def load_file(file_path):
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path,encoding= 'utf-8')

    return loader.load()

transcript_list = load_file(r"C:\Users\Dell\Downloads\Chatbot_Build_Plan.pdf") #file link or the local url
transcript = " ".join(chunk.page_content for chunk in transcript_list)


text_splitter = RecursiveCharacterTextSplitter(chunk_size = 200,chunk_overlap = 50)
chunks = text_splitter.create_documents([transcript])

vector_store = FAISS.from_documents(chunks,embeddings)

retrieve = vector_store.as_retriever(search_type = "similarity",search_kwargs ={"k":4})

message ="""
    You are a helpful assistent.
    Answer ONLY from the provided transcript context.
    if the context is insufficient, just say you don't know.

    {context}

    question:
    {question}
    """

question = "what' are we trying to make"

retrieve_doc = retrieve.invoke(question)

context = " ".join(doc.page_content for doc in retrieve_doc)

answer = chat_llm(message.format(context=context, question=question))

print(answer)

