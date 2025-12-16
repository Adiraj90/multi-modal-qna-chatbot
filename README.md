# 🤖 Multi-Modal QnA Chatbot

The **Multi-Modal QnA Chatbot** is an AI-powered web application built using **Streamlit** and **LangChain**.  
The main feature of this project is **multi-AI provider integration**, which means the chatbot is **not limited to a single AI model**. Users can switch between multiple AI providers such as **Groq, OpenAI, Google Gemini, Anthropic Claude, and Ollama (local models)** from the same interface.

The application supports real-world use cases like normal AI chat, context-aware conversations, internet-based QnA, document-based question answering, SQL database querying using natural language, and website content analysis.

---

## ✨ Features

- 🔁 **Multi-AI Provider Support** (Groq, OpenAI, Gemini, Claude, Ollama)
- 🤖 Basic AI Chat
- 🧠 Context-Aware Chat (remembers conversation)
- 🌐 Internet-Enabled QnA
- 📄 Chat with Documents (PDF, text files)
- 🗄️ Chat with SQL Databases using natural language
- 🌍 Chat with Website Content
- 🦙 Local AI support using Ollama (no API key required)

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- LangChain  
- SQLite  
- Pandas  
- Multiple LLM Providers  

---

## 📁 Project Structure

multi-modal-qna-chatbot/
│
├── Home.py                  # Main application entry
├── pages/                   # All chatbot feature pages
├── llm_providers.py         # Multi-AI provider handling
├── chat_utils.py            # Chat memory & session handling
├── streaming.py             # Streaming AI responses
├── assets/                  # Sample SQL database (Chinook)
├── requirements.txt
└── .streamlit/

---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/multi-modal-qna-chatbot.git
cd multi-modal-qna-chatbot
```

## 2️⃣ Create Virtual Environment

macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```
Windows
```bash 
python -m venv venv
venv\Scripts\activate
```
## 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## ✅ Create secrets.toml

Create the following file: .streamlit/secrets.toml

Add your API keys:
```toml
OPENAI_API_KEY = "your_openai_key"
GROQ_API_KEY = "your_groq_key"
GOOGLE_API_KEY = "your_google_key"
ANTHROPIC_API_KEY = "your_anthropic_key"
TAVILY_API_KEY = "your_tavily_key"
```
