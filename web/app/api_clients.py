"""Clientes HTTP de datos públicos. Se entregan los contratos, NO la solución."""
import json
import os
from pathlib import Path
import requests

GEO_URL = os.getenv("OPEN_METEO_GEO_URL", "https://geocoding-api.open-meteo.com/v1/search")
METEO_URL = os.getenv("OPEN_METEO_WEATHER_URL", "https://api.open-meteo.com/v1/forecast")
OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")


def geocodificar(ciudad: str) -> dict:
    response = requests.get(GEO_URL+f"?name={ciudad}&count=1&language=es&format=json", timeout=5)
    # Buscamos results
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "ciudad": str(result.get("name")),
                "pais":str(result.get("country")),
                "lat": float(result.get("latitude")),
                "lon": float(result.get("longitude"))
            }
    
    raise ValueError(f"No se encontraron resultados para la ciudad: {ciudad}")


def obtener_meteorologia(lat: float, lon: float) -> dict:
    response = requests.get(METEO_URL+f"?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto", timeout=5)
    if response.status_code == 200:
        data = response.json()
        if "current_weather" in data:
            current_weather = data["current_weather"]
            return {
                "temperatura_c": current_weather.get("temperature"),
                "precipitacion_mm": current_weather.get("precipitation"),
                "codigo_tiempo": current_weather.get("weathercode"),
                "instante": current_weather.get("time")
            }
    
    raise ValueError(f"No se pudo obtener la meteorología para lat: {lat}, lon: {lon}")


def obtener_lugares(lat: float, lon: float, tipo: str) -> list[dict]:
    """TODO(ALUMNADO).

    Consultar un radio urbano acotado de Overpass/OSM (2-3 km).
    Filtrar según tipo: cultural, gastronomica, naturaleza, familiar.
    Normalizar a [{nombre, categoria, lat, lon, fuente, ...}], máximo
    8-12 lugares. Gestionar nodos (lat/lon) y ways/relations (center).
    Nunca introducir valores libres del usuario en una consulta QL.
    """
    
    raise NotImplementedError("Implementa consulta de puntos de interés")


def cargar_fixture_lugares() -> list[dict]:
    """Utilidad entregada para simular Overpass durante pruebas sin Internet.

    Los lugares son FICTICIOS y deben identificarse como DEMO en la UI.
    """
    file_path = Path("/fixtures/puntos_demo.json")
    if not file_path.exists():
        file_path = Path(__file__).resolve().parents[2] / "fixtures/puntos_demo.json"
    return json.loads(file_path.read_text(encoding="utf-8"))["lugares"]
