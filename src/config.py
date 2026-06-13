# src/config.py
# Central configuration — all constants and keys live here

from dotenv import load_dotenv
import os

# Load keys from .env file
load_dotenv()

# API Keys
AEMET_API_KEY  = os.getenv("AEMET_API_KEY")
HF_TOKEN       = os.getenv("HF_TOKEN")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")

# LLM settings — same values you used in your notebook
LLM_MODEL   = "llama-3.1-8b-instant"
TEMPERATURE = 0.3
MAX_TOKENS  = 1024

# Embeddings & vector store
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DIR      = "chroma_db"

# Spain cities dictionary — copy this from your notebook
SPAIN_CITIES = {
    # Andalucía
    "Almería":       "04013",
    "Cádiz":         "11012",
    "Córdoba":       "14021",
    "Granada":       "18087",
    "Huelva":        "21041",
    "Jaén":          "23050",
    "Málaga":        "29067",
    "Sevilla":       "41091",
    # Aragón
    "Huesca":        "22125",
    "Teruel":        "44216",
    "Zaragoza":      "50297",
    # Asturias
    "Oviedo":        "33044",
    # Baleares
    "Palma":         "07040",
    # Canarias
    "Las Palmas":    "35016",
    "Santa Cruz":    "38038",
    # Cantabria
    "Santander":     "39075",
    # Castilla-La Mancha
    "Albacete":      "02003",
    "Ciudad Real":   "13034",
    "Cuenca":        "16078",
    "Guadalajara":   "19130",
    "Toledo":        "45168",
    # Castilla y León
    "Ávila":         "05019",
    "Burgos":        "09059",
    "León":          "24089",
    "Palencia":      "34120",
    "Salamanca":     "37274",
    "Segovia":       "40155",
    "Soria":         "42173",
    "Valladolid":    "47186",
    "Zamora":        "49275",
    # Cataluña
    "Barcelona":     "08019",
    "Girona":        "17079",
    "Lleida":        "25120",
    "Tarragona":     "43148",
    # Extremadura
    "Badajoz":       "06015",
    "Cáceres":       "10037",
    # Galicia
    "A Coruña":      "15030",
    "Lugo":          "27028",
    "Ourense":       "32054",
    "Pontevedra":    "36038",
    # La Rioja
    "Logroño":       "26089",
    # Madrid
    "Madrid":        "28079",
    # Murcia
    "Murcia":        "30030",
    # Navarra
    "Pamplona":      "31201",
    # País Vasco
    "Vitoria":       "01059",
    "San Sebastián": "20069",
    "Bilbao":        "48020",
    # Valencia
    "Alicante":      "03014",
    "Castellón":     "12040",
    "Valencia":      "46250",
    # Ceuta & Melilla
    "Ceuta":         "51001",
    "Melilla":       "52001",
}