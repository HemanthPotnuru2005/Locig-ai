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
    

def retrieve(question):
    retrieve = vector_store.as_retriever(search_type = "similarity",
                                         search_kwargs ={"k":4})

    return retrieve.invoke(question)


def final_prompt(context,question):
    prompt = PromptTemplate(
    template= """
    You are a helpful assistent.Answer ONLY from the provided transcript context.
    if the context is insufficient, just say you don't know.

    {context}
    question : {question}
    """,
    input_variables={'context','question'})

    prompt_value = prompt.invoke({
    "context": context,
    "question": question
})
    answer = chat_llm(prompt_value.to_string())    
    return answer


transcript_list = load_file(r"C:\Users\Dell\Downloads\Chatbot_Build_Plan.pdf") #file link or the local url
# call 1

transcript = " ".join(chunk.page_content for chunk in transcript_list)

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 200,chunk_overlap = 50)

chunks = text_splitter.create_documents([transcript])

vector_store = FAISS.from_documents(chunks,embeddings)

question = "what' are we trying to make"

retrieve_doc = retrieve(question) # call 2

context = " ".join(doc.page_content for doc in retrieve_doc)

answer = final_prompt(context,question)  # call 3

print(answer)
