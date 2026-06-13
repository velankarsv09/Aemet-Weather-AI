# src/aemet_client.py
# Handles all communication with the AEMET OpenData API

import requests
from src.config import AEMET_API_KEY

class AEMETClient:
    BASE_URL = "https://opendata.aemet.es/opendata/api"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"accept": "application/json"}
        self.params  = {"api_key": self.api_key}

    def _fetch(self, endpoint: str) -> dict:
        """AEMET two-step fetch: first call returns a data URL, second call returns actual data."""
        url = f"{self.BASE_URL}{endpoint}"
        r   = requests.get(url, headers=self.headers, params=self.params)
        r.raise_for_status()
        response = r.json()
        data_url = response.get("datos")
        if not data_url:
            return {}
        data_r = requests.get(data_url, headers=self.headers)
        data_r.raise_for_status()
        return data_r.json()

    def get_weather_by_city(self, municipio_code: str) -> dict:
        """Get hourly forecast for a Spanish municipality code."""
        endpoint = f"/prediccion/especifica/municipio/horaria/{municipio_code}"
        data = self._fetch(endpoint)
        return data[0] if data else {}

# Ready-to-use client instance
client = AEMETClient(AEMET_API_KEY)