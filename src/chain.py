# src/chain.py
# LLM setup and unified chain that combines live forecast + RAG context

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langdetect import detect
from src.config import GROQ_API_KEY, LLM_MODEL, TEMPERATURE, MAX_TOKENS
import time


# ── LLM instance ──────────────────────────────────────────────────────────────
llm = ChatGroq(
    model=LLM_MODEL,
    api_key=GROQ_API_KEY,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS
)


def filter_relevant_cities(question: str, forecast_data: dict) -> dict:
    """
    Return only cities mentioned in the question.
    If no city is detected, return all forecasts.
    """
    question_lower = question.lower()
    matches = {
        city: days
        for city, days in forecast_data.items()
        if city.lower() in question_lower
    }
    return matches if matches else forecast_data


def run_unified_chain(
    question: str,
    forecast_data: dict,
    retriever,
    llm,
    verbose: bool = True
) -> str:
    """
    Run the unified chain:
    1. Detect question language
    2. Retrieve RAG context from ChromaDB
    3. Filter relevant city forecasts
    4. Build prompt and invoke LLM
    """

    # Detect question language
    try:
        detected_language = detect(question)
    except Exception:
        detected_language = "en"

    # Retrieve RAG context
    retrieved_docs = retriever.invoke(question)
    rag_context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    if verbose:
        print(f"[RAG] Retrieved {len(retrieved_docs)} chunks from ChromaDB")

    # Filter forecast data to relevant cities
    relevant_forecasts = filter_relevant_cities(question, forecast_data)

    # Format forecast context
    forecast_text = ""
    for city, days in relevant_forecasts.items():
        forecast_text += f"\n### {city.upper()} FORECAST\n"
        for d in days[:2]:
            sky   = ", ".join(d["sky_conditions"]) if d["sky_conditions"] else "N/A"
            rain  = d["rain_probability"][:2] if d["rain_probability"] else "N/A"
            storm = d["storm_probability"][:2] if d["storm_probability"] else "N/A"
            forecast_text += (
                f"{d['date']}: {d['temp_min']}°C – {d['temp_max']}°C | "
                f"Sky: {sky} | Rain prob: {rain} | Storm prob: {storm}\n"
            )

    # Build prompt
    system_prompt = f"""
You are an expert weather assistant for Spain, specialising in AEMET data.

Question language: {detected_language}

You have two sources of information:

1. LIVE FORECAST DATA (from AEMET API):
{forecast_text}

2. AEMET ALERT & DOCUMENTATION CONTEXT (from official AEMET documents):
{rag_context if rag_context else "No relevant documents retrieved."}

RULES:
- Use BOTH sources together whenever relevant.
- Use forecast data when answering weather questions.
- Use retrieved documents when answering alert, warning, or AEMET policy questions.
- If information is unavailable, say so clearly.
- ALWAYS answer in the language specified above.
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ]

    # Retry logic for Groq rate limits
    for attempt in range(3):
        try:
            response = llm.invoke(messages)
            return response.content
        except Exception as e:
            error_text = str(e).lower()
            if "rate limit" in error_text or "429" in error_text or "too many requests" in error_text:
                print(f"[Retry {attempt+1}/3] Rate limit reached. Waiting 10 seconds...")
                time.sleep(10)
                continue
            raise

    return "Unable to generate a response after multiple retry attempts."