"""Punto ÚNICO de integración para web y API JSON. Pendiente del alumnado."""
from flask import abort

from app import api_clients, db, llm

TIPOS_VALIDOS = {"cultural", "gastronomica", "naturaleza", "familiar"}
DURACIONES_VALIDAS = {2, 4, 6}


def procesar_solicitud(ciudad: str, tipo_turismo: str, duracion_horas: int, preferencias: str = "") -> dict:
    """TODO(ALUMNADO): implementar todo el recorrido.

    1) Validación (ciudad no vacía, tipo permitido, duración 2/4/6).
    
    
    2) Geocodificar la ciudad y consultar clima actual.
    3) Consultar lugares reales; si falla Overpass, utilizar fixture
       SOLAMENTE para demostrar flujo, marcando 'demo': True.
    4) Preparar el contexto y llamar a llm.generar_itinerario.
    5) Guardar entradas, respuestas, prompt, resultado, éxito/error,
       duración y el modo de datos en PostgreSQL.
    6) Devolver contrato consistente a ambas rutas Flask.

    Salida orientativa:
      {'ciudad': ..., 'tipo_turismo': ..., 'meteorologia': {...},
       'lugares': [...], 'itinerario': ..., 'modo_demo': False,
       'solicitud_id': 1}

    IMPORTANTE: ni el modelo ni los mocks son la fuente de lugares.
    Los datos de interés proceden de Overpass; el modelo los ORGANIZA.
    """
    # 1 Validacion
    if ciudad.strip() == "":
        abort(400, description="La ciudad no puede estar vacía")
    if tipo_turismo not in TIPOS_VALIDOS:
        abort(400, description=f"Tipo de turismo no válido: {tipo_turismo}")
    if duracion_horas not in DURACIONES_VALIDAS:
        abort(400, description=f"Duración no válida: {duracion_horas}")
    
    # 2 Geocodificación y meteorología
    coordenadas = api_clients.geocodificar(ciudad)
    meteorologia = api_clients.obtener_meteorologia(coordenadas['lat'], coordenadas['lon'])
    
    # 3 Consulta de lugares
    try: 
      lugares = api_clients.obtener_lugares(coordenadas['lat'], coordenadas['lon'], tipo_turismo)
      modo_demo = False
    except Exception as e:
      print(f"Error al consultar Overpass: {e}. Usando fixture de demo.")
      lugares = api_clients.cargar_fixture_lugares()
      modo_demo = True
    
    # 4 Preparar contexto y llamar a llm
    
    
    raise NotImplementedError("Implementa el flujo de integración")
