# Locig-AI

A personal learning project for understanding how to work with LLMs using LangChain and Groq, with RAG planned next.

## Why this project

I made this for my own understanding, to learn how these pieces work. It is not meant to be a polished or showcase project. All the code was written by me without using any AI tools.

Still in progress.

## Files

- `llm.py` - sets up the Groq model (`openai/gpt-oss-20b`) and a `chat_llm()` helper
- `rag.py` - RAG part (not written yet)
- `app.py` - app part (not written yet)
- `sample.py` - scratch file

## Run

```bash
pip install langchain-groq python-dotenv
```

Put your key in a `.env` file:

```
GROQ_API_KEY=your_key
```

```python
from llm import chat_llm

chat_llm("Hello")
```
