"""Punto único de integración para web y API JSON."""
from flask import abort

from app import api_clients, db, llm

TIPOS_VALIDOS = {"cultural", "gastronomica", "naturaleza", "familiar"}
DURACIONES_VALIDAS = {2, 4, 6}


def procesar_solicitud(ciudad: str, tipo_turismo: str, duracion_horas: int, preferencias: str = "") -> dict:
    """Valida, obtiene datos, genera el itinerario y guarda la solicitud."""
    if not isinstance(ciudad, str) or not ciudad.strip():
        abort(400, description="La ciudad no puede estar vacía")
    ciudad = ciudad.strip()
    if len(ciudad) > 80:
        abort(400, description="La ciudad no puede superar 80 caracteres")
    if not isinstance(tipo_turismo, str) or tipo_turismo not in TIPOS_VALIDOS:
        abort(400, description=f"Tipo de turismo no válido: {tipo_turismo}")
    if (
        isinstance(duracion_horas, bool)
        or not isinstance(duracion_horas, int)
        or duracion_horas not in DURACIONES_VALIDAS
    ):
        abort(400, description=f"Duración no válida: {duracion_horas}")
    if not isinstance(preferencias, str) or len(preferencias) > 200:
        abort(400, description="Las preferencias no pueden superar 200 caracteres")

    coordenadas = api_clients.geocodificar(ciudad)
    latitud = coordenadas["lat"]
    longitud = coordenadas["lon"]
    meteorologia = api_clients.obtener_meteorologia(latitud, longitud)
    try:
        lugares = api_clients.obtener_lugares(latitud, longitud, tipo_turismo)
    except (ValueError, api_clients.requests.exceptions.RequestException):
        lugares = api_clients.cargar_fixture_lugares()
    modo_demo = any(lugar.get("demo", False) for lugar in lugares)

    contexto = {
        "ciudad": coordenadas.get("ciudad", ciudad),
        "pais": coordenadas.get("pais"),
        "tipo_turismo": tipo_turismo,
        "duracion_horas": duracion_horas,
        "preferencias": preferencias,
        "meteorologia": meteorologia,
        "lugares": lugares,
    }
    itinerario, prompt_usado = llm.generar_itinerario(contexto)

    registro = {
        "ciudad": contexto["ciudad"],
        "pais": contexto["pais"],
        "tipo_turismo": tipo_turismo,
        "duracion_horas": duracion_horas,
        "preferencias": preferencias,
        "latitud": latitud,
        "longitud": longitud,
        "meteorologia": meteorologia,
        "lugares": lugares,
        "prompt_usado": prompt_usado,
        "itinerario": itinerario,
        "modo_demo": modo_demo,
        "modo_modelo": llm.LLM_MODE,
        "estado": "completada",
        "duracion_ms": None,
        "error_resumido": None,
    }
    solicitud_id = db.guardar_solicitud(registro)

    return {
        "solicitud_id": solicitud_id,
        **contexto,
        "latitud": latitud,
        "longitud": longitud,
        "itinerario": itinerario,
        "prompt_usado": prompt_usado,
        "modo_demo": modo_demo,
        "modo_modelo": llm.LLM_MODE,
        "estado": "completada",
        "duracion_ms": None,
    }
