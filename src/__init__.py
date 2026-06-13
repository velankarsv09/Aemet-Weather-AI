# src/__init__.py
# Makes src a Python package and exposes key imports

from src.aemet_client import client
from src.forecast_parser import get_forecast_summary
from src.vectorstore import load_embeddings, build_vectorstore, load_vectorstore, get_retriever
from src.chain import llm, run_unified_chain