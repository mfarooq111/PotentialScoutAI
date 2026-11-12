from config.models import llm

response = llm.invoke(
    "Explain what a RAG chatbot is in two sentences."
)

print(response.content)