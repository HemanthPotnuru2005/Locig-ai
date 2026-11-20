# Import Streamlit library for the web UI
import streamlit as st
from rag import retrieve, final_prompt
from llm import chat_llm

# Configure browser page title and icon
st.set_page_config(page_title="RAG & LLM Chatbot", page_icon="🤖")

# Display main app title
st.title("🤖 AI Chatbot")

# Display a subtitle description
st.caption("Streamlit interface connected with rag.py and llm.py")

# Add a sidebar title for controls
st.sidebar.title("⚙️ Options")

# Radio button to select between RAG mode and Normal Chat mode
mode = st.sidebar.radio("Choose Mode:", ["RAG Mode", "Normal Chat Mode"])

# Button to clear conversation history
if st.sidebar.button("Clear Chat"):
    # Reset message list in session state
    st.session_state["messages"] = []
    # Rerun the app to refresh display
    st.rerun()

# Check if message history exists in session state
if "messages" not in st.session_state:
    # Initialize empty message list
    st.session_state["messages"] = []

# Loop through past messages
for msg in st.session_state["messages"]:
    # Render chat bubble for sender role
    with st.chat_message(msg["role"]):
        # Display message text
        st.write(msg["content"])

# Chat input box at the bottom of page
user_input = st.chat_input("Type your message here...")

# Process user question when submitted
if user_input:
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Display user chat bubble
    with st.chat_message("user"):
        # Print user message text
        st.write(user_input)

    # Display assistant chat bubble
    with st.chat_message("assistant"):
        # Show spinner while generating response
        with st.spinner("Thinking..."):
            # Check if RAG Mode is selected
            if mode == "RAG Mode":
                # Retrieve relevant document chunks from rag.py
                retrieved_docs = retrieve(user_input)
                # Combine chunks into one context string
                context = " ".join([doc.page_content for doc in retrieved_docs])
                # Generate response using final_prompt from rag.py
                response = final_prompt(context, user_input)
            # If Normal Chat Mode is selected
            else:
                # Generate response using chat_llm from llm.py
                response = chat_llm(user_input)

            # Print assistant response text
            st.write(response)
            # Add assistant response to history
            st.session_state["messages"].append({"role": "assistant", "content": response})
