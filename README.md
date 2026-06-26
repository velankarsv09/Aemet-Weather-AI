# 🌤️ AEMET Weather AI Assistant

An AI-powered weather assistant for Spain that combines live weather data from 
AEMET (Spain's national meteorological service) with a RAG pipeline over official 
weather alert documents.

## 🚀 Features

- **Live weather data** — real-time forecasts for all 52 Spanish provinces via AEMET OpenData API
- **RAG pipeline** — semantic search over official AEMET alert PDFs using ChromaDB
- **Natural language Q&A** — ask weather questions in English or Spanish
- **Multilingual** — automatically detects and responds in the language of the question
- **Multi-city comparison** — compare weather across multiple Spanish cities simultaneously
- - **Conversational memory** — multi-turn chat with session history via LangChain memory
- **Agent with tools** — LLM autonomously selects the right tool per query

## 🛠️ Tech Stack

| Component 
| 
Technology 
|
|
|
---
|
| LLM 
| 
LLaMA 3.1 8B via Groq API 
|
| 
Embeddings 
| 
sentence-transformers/all-MiniLM-L6-v2
|
| 
Vector Store 
| 
ChromaDB 
|
| 
Framework 
| 
LangChain 
|
| 
Data Source  
| 
AEMET OpenData API 
|
| 
Language Detection 
| 
langdetect 
|

## 📁 Project Structure
