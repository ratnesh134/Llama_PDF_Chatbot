import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import UnstructuredPDFLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

working_dir = os.path.dirname(os.path.abspath(__file__))

def load_documents(file_paths):
    documents = []
    for file_path in file_paths:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            loader = UnstructuredPDFLoader(file_path)
        elif ext == ".docx":
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            continue  # skip unsupported files
        documents.extend(loader.load())
    return documents

def setup_vectorstore(documents):
    embeddings = HuggingFaceEmbeddings()
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200
    )
    doc_chunks = text_splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(doc_chunks, embeddings)
    return vectorstore

def create_chain(vectorstore):
    llm = ChatGroq(
        model='llama-3.3-70b-versatile',
        temperature=0,
    )
    retriever = vectorstore.as_retriever()
    memory = ConversationBufferMemory(
        output_key="answer",
        memory_key="chat_history",
        return_messages=True
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        verbose=True
    )
    return chain

st.set_page_config(
    page_title="Chat With Doc",
    page_icon="📝",
    layout="centered"
)

st.title("🦙 Llama PDF/DOCX Chatbot")

# Initialize the chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_files = st.file_uploader(
    label="Upload your PDF or DOCX files",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

file_paths = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(working_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_paths.append(file_path)

    if "vectorstore" not in st.session_state or st.session_state.get("uploaded_files") != [f.name for f in uploaded_files]:
        documents = load_documents(file_paths)
        st.session_state.vectorstore = setup_vectorstore(documents)
        st.session_state.conversation_chain = create_chain(st.session_state.vectorstore)
        st.session_state.uploaded_files = [f.name for f in uploaded_files]

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask Llama...")

if user_input:
    if not uploaded_files:
        st.error("Please upload at least one PDF or DOCX file before asking a question.")
    else:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response = st.session_state.conversation_chain({"question": user_input})
            assistant_response = response["answer"]
            st.markdown(assistant_response)
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})