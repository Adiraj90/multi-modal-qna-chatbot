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
```bash
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
```
---
## 🤖 AI Providers

The chatbot is designed with **multi-provider AI support**, allowing users to switch between different large language models at runtime without changing the application logic.

### 🔹 OpenAI (Cloud)
- Requires an API key  
- Supports models like **GPT-3.5**, **GPT-4**, and **GPT-4o**  
- Strong reasoning and context handling  
- Best suited for production-grade conversations and complex queries  

### ⚡ Groq (Cloud)
- Requires an API key (free tier available)  
- Ultra-fast inference with low latency  
- Ideal for real-time responses and SQL generation  
- Recommended default provider for speed  

### 🌐 Google Gemini (Cloud)
- Requires an API key  
- Supports **Gemini Pro** and **Gemini 1.5** models  
- Good multimodal and analytical capabilities  

### 🧠 Anthropic Claude (Cloud)
- Requires an API key  
- Known for safer responses and strong reasoning  
- Useful for long-form and structured explanations  

### 🦙 Ollama (Local)
- Runs entirely on the local machine  
- No API key required  
- Supports models like **TinyLlama**, **Llama 3**, **Mistral**  
- Ideal for offline usage, testing, and privacy-focused workflows  

---

## 🎨 Customization & Controls

### 🌡️ Temperature Control
The creativity of responses can be adjusted using the temperature parameter:

- **0.0** → Highly precise and deterministic  
- **0.7** → Balanced and natural conversations (default)  
- **1.0** → More creative and diverse outputs  

### 🧩 Model Selection
- Choose different models within the same provider  
- Switch between providers in real time from the sidebar  
- No application restart required  

This flexibility allows users to experiment with multiple AI models and select the best one for their specific use case.

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
## 🚀 Running the Application

After cloning the repository and installing dependencies, the application can be started using:

```bash
streamlit run Home.py
```
---
