import os
import tempfile
import streamlit as st
from document_loader import load_pdf
from rag_pipeline import split_documents, answer_question
from vector_store import create_vector_store
st.set_page_config(
    page_title="Academic Study Assistant",
    page_icon="📚",
    layout="wide"
)
def initialize_session():
    if "index" not in st.session_state:
        st.session_state.index = None
    if "embedding_model" not in st.session_state:
        st.session_state.embedding_model = None
    if "chunks" not in st.session_state:
        st.session_state.chunks = []
    if "messages" not in st.session_state:
        st.session_state.messages = []
initialize_session()
st.title("📚 Academic Study Assistant")
st.write(
    "Upload your college notes, syllabi, or textbooks in PDF format "
    "and ask questions based on their content."
)
with st.sidebar:
    st.header("Upload Study Materials")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )
    process_button = st.button(
        "Process PDFs",
        type="primary",
        use_container_width=True
    )
    if process_button:
        if not uploaded_files:
            st.warning("Please upload at least one PDF.")
        else:
            all_documents = []
            failed_files = []
            with st.spinner("Reading your PDF documents..."):
                for uploaded_file in uploaded_files:
                    temporary_path = None
                    try:
                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".pdf"
                        ) as temporary_file:
                            temporary_file.write(
                                uploaded_file.getvalue()
                            )
                            temporary_path = temporary_file.name
                        documents = load_pdf(temporary_path)
                        for document in documents:
                            document["source"] = uploaded_file.name
                        all_documents.extend(documents)
                    except Exception as error:
                        failed_files.append(
                            f"{uploaded_file.name}: {error}"
                        )
                    finally:
                        if (
                            temporary_path
                            and os.path.exists(temporary_path)
                        ):
                            os.remove(temporary_path)
            if failed_files:
                for message in failed_files:
                    st.error(f"Could not read PDF: {message}")
            if not all_documents:
                st.error(
                    "No extractable text was found in the uploaded PDFs."
                )
            else:
                with st.spinner(
                    "Creating text chunks and searching index..."
                ):
                    chunks = split_documents(all_documents)
                    index, embedding_model = create_vector_store(
                        chunks
                    )
                    st.session_state.index = index
                    st.session_state.embedding_model = embedding_model
                    st.session_state.chunks = chunks
                    st.session_state.messages = []
                st.success(
                    f"Processed {len(uploaded_files) - len(failed_files)} "
                    f"PDF file(s) and created {len(chunks)} text chunks."
                )
    st.divider()
    if st.session_state.chunks:
        st.success("Study materials are ready.")
        st.write(
            f"**Text chunks:** {len(st.session_state.chunks)}"
        )
        if st.button("Clear study materials"):
            st.session_state.index = None
            st.session_state.embedding_model = None
            st.session_state.chunks = []
            st.session_state.messages = []
            st.rerun()
if st.session_state.index is None:
    st.info(
        "Start by uploading one or more PDFs in the sidebar "
        "and clicking **Process PDFs**."
    )
else:
    st.subheader("Ask Your Study Question")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                sources = message.get("sources", [])
                if sources:
                    with st.expander("View PDF sources"):
                        for source in sources:
                            st.write(
                                f"- **{source['source']}** — "
                                f"Page {source['page']}"
                            )

    question = st.chat_input(
        "Ask a question about your uploaded notes..."
    )
    if question:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Finding an answer in your PDFs..."):
                    answer, sources = answer_question(
                        question,
                        st.session_state.index,
                        st.session_state.embedding_model,
                        st.session_state.chunks
                    )
                st.markdown(answer)
                if sources:
                    with st.expander("View PDF sources"):
                        for source in sources:
                            st.write(
                                f"- **{source['source']}** — "
                                f"Page {source['page']}"
                            )
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    }
                )
            except Exception as error:
                st.error(
                    "Unable to generate an answer. "
                    "Check your Groq API configuration and try again."
                )
                st.caption(str(error))