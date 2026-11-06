"""Pruebas básicas proporcionadas. Completar con 2 tests más por pareja."""
import sys
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import api_clients, orchestrator
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


def test_orquestador_usa_fixture_si_falla_overpass(monkeypatch):
    lugares_demo = [
        {
            "nombre": "Museo de Ejemplo (DEMO)",
            "categoria": "museum",
            "lat": 39.4702,
            "lon": -0.3759,
            "fuente": "fixture",
            "demo": True,
        }
    ]
    monkeypatch.setattr(
        orchestrator.api_clients,
        "geocodificar",
        lambda ciudad: {
            "ciudad": ciudad,
            "pais": "España",
            "lat": 39.47,
            "lon": -0.37,
        },
    )
    monkeypatch.setattr(
        orchestrator.api_clients,
        "obtener_meteorologia",
        lambda lat, lon: {"temperatura_c": 18, "precipitacion_mm": 0},
    )
    monkeypatch.setattr(
        orchestrator.api_clients,
        "obtener_lugares",
        Mock(side_effect=ValueError("Overpass no disponible")),
    )
    monkeypatch.setattr(
        orchestrator.api_clients, "cargar_fixture_lugares", lambda: lugares_demo
    )
    generar_itinerario = Mock(return_value=("Ruta demo", "Prompt demo"))
    guardar_solicitud = Mock(return_value=123)
    monkeypatch.setattr(orchestrator.llm, "generar_itinerario", generar_itinerario)
    monkeypatch.setattr(orchestrator.db, "guardar_solicitud", guardar_solicitud)

    resultado = orchestrator.procesar_solicitud("Valencia", "cultural", 4)

    assert resultado["lugares"] == lugares_demo
    assert resultado["modo_demo"] is True
    assert resultado["solicitud_id"] == 123
    assert generar_itinerario.call_args.args[0]["lugares"] == lugares_demo
    assert guardar_solicitud.call_args.args[0]["lugares"] == lugares_demo
