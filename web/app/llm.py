"""Adaptador Cohere. El PROMPT lo redacta el alumnado."""
import os
import requests

LLM_MODE = os.getenv("LLM_MODE", "mock").lower()
COHERE_MODEL = os.getenv("COHERE_MODEL", "command-r7b-12-2024")
COHERE_API_URL = "https://api.cohere.com/v2/chat"

def _construir_prompt(contexto: dict) -> str:
    ciudad = contexto.get("ciudad", "la ciudad")
    tipo = contexto.get("tipo_turismo", "general")
    duracion = contexto.get("duracion_horas", 4)
    preferencias = contexto.get("preferencias", "ninguna")
    clima = contexto.get("meteorologia", {})
    lugares = contexto.get("lugares", [])

    temp = clima.get("temperatura_c", "desconocida")
    precip = clima.get("precipitacion_mm", 0)

    num_lugares = len(lugares)
    if lugares:
        lista_lugares_str = "\n".join(
            f"- {l.get('nombre', 'Sin nombre')} (Categoría: {l.get('categoria', 'general')})"
            for l in lugares
        )
    else:
        lista_lugares_str = "NINGUNO. La lista está vacía."

    prompt = f"""Eres CityPilot, un asistente estricto de rutas urbanas.
Tu tarea es proponer un itinerario usando ÚNICAMENTE los lugares verificados que te proporciono.

DATOS DE LA SOLICITUD:
- Ciudad: {ciudad}
- Tipo de experiencia: {tipo}
- Tiempo previsto: {duracion} horas
- Preferencias: {preferencias if preferencias else 'Sin preferencias'}
- Clima: {temp} °C, precipitación: {precip} mm

LUGARES REALES VERIFICADOS DISPONIBLES ({num_lugares} disponibles):
{lista_lugares_str}

REGLAS ABSOLUTAS (INCUMPLIRLAS INVALIDA TU RESPUESTA):
1. REGLA ANTI-ALUCINACIÓN: Si hay menos de 3 lugares disponibles en la lista, NO INVENTES NINGÚN LUGAR NUEVO. En su lugar, indica claramente: "Aviso: no hay suficientes lugares verificados disponibles en la base de datos para una ruta completa de {duracion} horas", y describe únicamente el/los sitios que sí están en la lista.
2. Si hay 3 o más lugares, selecciona entre 3 y 5 lugares EXCLUSIVAMENTE de la lista. Queda terminantemente prohibido añadir plazas, parques, calles o monumentos que no aparezcan arriba.
3. ADAPTACIÓN AL CLIMA: Comenta el clima de forma realista ({temp} °C y {precip} mm). Si llueve (> 0 mm), prioriza interiores. Si está despejado y templado, no digas que hace calor extremo.
4. FORMATO:
   - Resumen y justificación del clima.
   - Itinerario con las paradas verificadas y tiempo orientativo.
   - Consejos breves.

Responde en castellano:"""

    return prompt

def generar_itinerario(contexto: dict) -> tuple[str, str]:
    """Devuelve (texto_itinerario, prompt_usado).

    `contexto` incluye: ciudad, tipo_turismo, duracion_horas,
    preferencias, meteorologia y lista de lugares REALES de la fuente.
    """
    if LLM_MODE == "mock":
        return _simulador(contexto), "[SIMULADOR: sin llamada a modelo]"

    if LLM_MODE != "cohere":
        raise ValueError("LLM_MODE debe ser 'mock' o 'cohere'")

    api_key = os.getenv("COHERE_API_KEY", "")
    if not api_key:
        raise RuntimeError("Falta COHERE_API_KEY (pedirla al docente)")

    prompt = _construir_prompt(contexto)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": COHERE_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    try:
        response = requests.post(
            COHERE_API_URL,
            headers=headers,
            json=payload,
            timeout=20,
        )

        if response.status_code == 401:
            raise RuntimeError("Error 401 de autenticación en Cohere: COHERE_API_KEY no válida.")
        elif response.status_code == 429:
            raise RuntimeError("Error 429: Se ha superado la cuota de peticiones de Cohere.")
        response.raise_for_status()
        
        data = response.json()
        contenido = data.get("message", {}).get("content", [])
        if not contenido or not isinstance(contenido, list):
            raise ValueError("Cohere devolvió una respuesta sin contenido estructurado.")
        texto_itinerario = contenido[0].get("text", "").strip()
        if not texto_itinerario:
            raise ValueError("Cohere devolvió un texto de respuesta vacío.")
        return texto_itinerario, prompt
    
    except requests.exceptions.Timeout:
        raise RuntimeError("Tiempo de espera agotado al conectar con Cohere (Timeout).")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error de conexión con la API de Cohere: {e}")

def _simulador(contexto: dict) -> str:
    """Salida no generativa para pruebas y para cuando no hay credenciales."""
    lugares = contexto.get("lugares") or []
    ciudad = contexto.get("ciudad", "la ciudad")
    tipo = contexto.get("tipo_turismo", "libre")
    nombres = [x.get("nombre", "Lugar sin nombre") for x in lugares[:4]]
    visitas = "\n".join(f"{i}. {nombre}" for i, nombre in enumerate(nombres, 1))
    if not visitas:
        visitas = "No hay lugares verificados disponibles."
    return f"[MODO SIMULACIÓN - NO ES IA]\nPlan {tipo} en {ciudad}:\n{visitas}"
