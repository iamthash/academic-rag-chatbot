# Academic Study Assistant — PDF Question Answering with RAG

## Overview

Academic Study Assistant is a domain-specific Retrieval-Augmented Generation (RAG) chatbot that helps students ask questions about academic notes, syllabi, and textbooks in PDF format.

The application retrieves relevant passages from uploaded PDFs and uses a language model through the Groq API to generate answers grounded in the retrieved content.

## Problem Statement

Students often spend time searching through lengthy academic PDFs to find definitions, explanations, and important concepts. This project provides a simple interface where students can upload study materials and ask questions in natural language.

## Features

- Upload one or more PDF documents.
- Extract text from PDF pages.
- Split document text into smaller chunks.
- Generate embeddings using Sentence Transformers.
- Retrieve relevant passages using FAISS similarity search.
- Generate answers using the Groq API.
- Display source PDF filenames and page numbers.
- Maintain conversation history during the current app session.
- Handle questions when relevant information is missing from the documents.

## Technologies Used

- Python
- Streamlit
- PyPDF
- LangChain Text Splitters
- Sentence Transformers (`all-MiniLM-L6-v2`)
- FAISS
- Groq API
- python-dotenv
- pandas

## Project Structure

```text
academic_rag_chatbot/
├── app.py
├── rag_pipeline.py
├── document_loader.py
├── vector_store.py
├── prompt.py
├── requirements.txt
├── README.md
├── .gitignore
├── documents/
├── vector_store/
└── tests/
    └── test_questions.csv
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/iamthash/academic-rag-chatbot.git
cd academic-rag-chatbot
```

### 2. Create a virtual environment

Python 3.12 is recommended.

**Windows PowerShell:**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a local file named `.env` in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Replace the placeholder with your own API key. Obtain a key through the Groq Console.

**Security:** Never upload `.env` to GitHub or share your API key publicly.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, upload your academic PDFs, click **Process PDFs**, and start asking questions.

## How It Works

1. **PDF Upload:** The user uploads academic PDF documents.
2. **Text Extraction:** PyPDF extracts text from each page.
3. **Text Chunking:** LangChain splits extracted text into overlapping chunks.
4. **Embedding Generation:** Sentence Transformers converts chunks into numerical vectors.
5. **Similarity Search:** FAISS retrieves passages relevant to the user's question.
6. **Answer Generation:** The Groq API generates an answer using the retrieved context and system prompt.
7. **Source Display:** The application displays relevant PDF filenames and page numbers.

## Testing and Evaluation

The application was tested using college study materials in PDF format.

Five test scenarios were used to evaluate:
- Questions whose answers are available in the document.
- Questions about related concepts.
- Questions about missing information.
- Application-based questions.
- Unrelated questions to check how the system handles unsupported information.

The expected behavior is to provide relevant answers grounded in the uploaded PDFs and indicate when requested information cannot be found.

## Limitations

- Scanned PDFs may require OCR if they do not contain extractable text.
- Answer quality depends on PDF text quality, retrieval relevance, and the language model.
- The application requires a valid Groq API key and internet access for answer generation.
- Retrieved passages may not always contain enough information to answer every question correctly.

## Future Enhancements

- OCR support for scanned PDFs.
- Subject and document filters.
- Improved retrieval evaluation.
- User feedback and answer ratings.
- Persistent vector indexes.
- Deployment for access outside the local computer.

## Responsible AI and Security

The system is designed to answer questions using retrieved document context and to treat instructions embedded in PDF content as untrusted data. Users should keep API keys private and upload only documents they are authorized to use.

## Author

**Thashan Sai**

GitHub: [@iamthash](https://github.com/iamthash)

Project Repository: [academic-rag-chatbot](https://github.com/iamthash/academic-rag-chatbot)
