"""Pruebas básicas proporcionadas. Completar con 2 tests más por pareja."""
import sys
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import api_clients
from app.main import create_app


def test_inicio_responde():
    client = create_app().test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"CityPilot" in response.data


def test_analitica_responde():
    client = create_app().test_client()
    assert client.get("/analitica").status_code == 200


def test_geocodificar_mapea_resultado(monkeypatch):
    respuesta = Mock()
    respuesta.status_code = 200
    respuesta.json.return_value = {
        "results": [
            {
                "name": "Madrid",
                "country": "España",
                "latitude": 40.4168,
                "longitude": -3.7038,
            }
        ]
    }
    llamada_get = Mock(return_value=respuesta)
    monkeypatch.setattr(api_clients.requests, "get", llamada_get)

    resultado = api_clients.geocodificar("Madrid")

    assert resultado == {
        "ciudad": "Madrid",
        "pais": "España",
        "lat": 40.4168,
        "lon": -3.7038,
    }
    llamada_get.assert_called_once()


def test_obtener_meteorologia_mapea_clima_actual(monkeypatch):
    respuesta = Mock()
    respuesta.status_code = 200
    respuesta.json.return_value = {
        "current_weather": {
            "temperature": 18.5,
            "precipitation": 2.0,
            "weathercode": 61,
            "time": "2025-05-01T12:00",
        }
    }
    llamada_get = Mock(return_value=respuesta)
    monkeypatch.setattr(api_clients.requests, "get", llamada_get)

    resultado = api_clients.obtener_meteorologia(40.4168, -3.7038)

    assert resultado == {
        "temperatura_c": 18.5,
        "precipitacion_mm": 2.0,
        "codigo_tiempo": 61,
        "instante": "2025-05-01T12:00",
    }
    llamada_get.assert_called_once()

