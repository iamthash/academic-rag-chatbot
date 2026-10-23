import os
from dotenv import load_dotenv
from groq import Groq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from prompt import SYSTEM_PROMPT
from vector_store import search_similar
load_dotenv()
def split_documents(documents, chunk_size=900, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = []
    for document in documents:
        text_chunks = splitter.split_text(document["text"])
        for chunk in text_chunks:
            chunks.append({
                "text": chunk,
                "source": document["source"],
                "page": document["page"]
            })

    return chunks
def answer_question(question, index, model, chunks):
    if not question.strip():
        return "Please enter a question.", []
    results = search_similar(
        question,
        index,
        model,
        chunks,
        k=4
    )
    if not results:
        return (
            "I could not find the answer in the uploaded documents.",
            []
        )
    context_parts = []
    for result in results:
        context_parts.append(
            f"Source: {os.path.basename(result['source'])}\n"
            f"Page: {result['page']}\n"
            f"Content:\n{result['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to your .env file."
        )
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n"
                    f"Retrieved PDF context:\n{context}"
                )
            }
        ],
        temperature=0.1
    )
    answer = response.choices[0].message.content
    return answer, results