# src/forecast_parser.py
# Parses raw AEMET API responses into clean LLM-friendly summaries

def parse_daily_forecast(day: dict) -> dict:
    """Convert raw AEMET day data into a clean LLM-friendly summary."""
    temps = [int(t["value"]) for t in day.get("temperatura", []) if t.get("value")]
    sky   = list(set([s["descripcion"] for s in day.get("estadoCielo", []) if s.get("descripcion")]))
    rain  = [f"Period {r['periodo']}: {r['value']}%" for r in day.get("probPrecipitacion", []) if r.get("value")]
    storm = [f"Period {s['periodo']}: {s['value']}%" for s in day.get("probTormenta", []) if s.get("value")]
    return {
        "date":             day.get("fecha", "")[:10],
        "temp_min":         min(temps) if temps else None,
        "temp_max":         max(temps) if temps else None,
        "sky_conditions":   sky,
        "rain_probability": rain,
        "storm_probability":storm,
        "sunrise":          day.get("orto"),
        "sunset":           day.get("ocaso"),
    }


def get_forecast_summary(weather_data: dict) -> list:
    """Parse all available days from an AEMET city response."""
    days = weather_data.get("prediccion", {}).get("dia", [])
    return [parse_daily_forecast(day) for day in days]