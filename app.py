import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings, HuggingFaceInstructEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
import torch

load_dotenv()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            extracted_text = page.extract_text() or ""
            text += extracted_text + "\n"
    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_conversation_chain(vectorstore, use_openai=False):
    if use_openai:
        llm = ChatOpenAI()
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-base",
        model_kwargs={
            'temperature': 0.5,
            'max_length': 512,
        }
    )


    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
    )

    return conversation_chain

def get_vector_store(text_chunks):
    # Check if CUDA is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Initialize embeddings with GPU support if available
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': device}
    )

    # Create vector store
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.error("Please upload PDFs and click on Process first.")
        return

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.header("Chat with multiple PDFs :books:")

    st.write(css, unsafe_allow_html=True)

    # Initialize session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = None

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None

    # Display current device being used
    device = 'GPU (CUDA)' if torch.cuda.is_available() else 'CPU'
    st.sidebar.info(f'Running on: {device}')

    user_question = st.text_input("Ask a question about your PDF")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Uploaded documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here, then click on Process",
            accept_multiple_files=True,
            type=['pdf']
        )
        if st.button("Process Documents", type="primary"):
            if not pdf_docs:
                st.error("Please upload at least one PDF file.")
                return

            with st.spinner("Processing..."):
                try:
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vector_store(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vectorstore, use_openai=False)
                    st.success("Processing complete!")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
