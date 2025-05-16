
# 🦙 Llama PDF/DOCX Chatbot

A Streamlit-based conversational AI app that lets you chat with the contents of your uploaded PDF and DOCX documents using Llama-3 via LangChain and Groq.

## 🚀 Features
Chat with multiple PDFs and DOCX files
Conversational memory: Maintains chat history for context
Supports Llama-3 via Groq
User-friendly Streamlit interface
Error handling: Prompts users to upload documents before asking questions

## 🛠️ Installation
1. Clone the repository
git clone https://github.com/yourusername/llama-pdf-docx-chatbot.git
cd llama-pdf-docx-chatbot

2. Create and activate a virtual environment (Python 3.10 recommended)
python3.10 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt


## Sample requirements.txt:

streamlit
langchain
langchain-community
langchain-groq
python-dotenv
pdfminer.six==20221105
unstructured==0.10.30
python-docx

## ⚙️ Environment Variables

Create a .env file in the project root and add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here

🏃‍♂️ Usage
streamlit run app.py

Open the web interface in your browser.
Upload one or more PDF or DOCX files.
Ask questions about your documents in natural language.

## 📂 Project Structure
llama-pdf-docx-chatbot/
├── app.py
├── requirements.txt
├── .env
└── README.md

## 📝 Notes
Only PDF and DOCX files are supported.
If you ask a question before uploading any document, the app will prompt you to upload files.
For best results, use clear and well-formatted documents.

## 🤝 Contributing

Pull requests and issues are welcome! Please open an issue to discuss your ideas or report bugs.


Happy chatting with your documents!
