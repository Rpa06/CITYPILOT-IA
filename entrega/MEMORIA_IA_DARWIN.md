# Memoria individual de utilización de IA — CityPilot IA

> **Rellenad una copia de este documento POR PERSONA** y guardadla como `entrega/MEMORIA_IA_<NOMBRE>.md`. Actividad de **semáforo amarillo**. Puede utilizarse IA como asistencia, pero debe quedar documentada con precisión. No incluyáis secretos. Si no habéis usado IA, decidlo expresamente y justificad el trabajo propio con evidencias.

## 1. Autoría y aportación individual

- Estudiante: Darwin Alonso Chavez Santillan
- Equipo: Hugo, Cristofer, Rafael
- Repositorio GitHub: https://github.com/Rpa06/CITYPILOT-IA
- Mis dos PR, con revisión cruzada: https://github.com/Rpa06/CITYPILOT-IA/pull/3 y [PR 2]
- Archivos o funciones que implementé personalmente: llm.py
- Pruebas que ejecuté personalmente y resultado: 
    - Prueba de integración en Docker"
    - Prueba de estrés con datos insuficientes con 1 solo lugar verificado, validando que el modelo emite la advertencia obligatoria y no inventa lugares adicionales.
    - Verificación de autenticación y consumo real de tokens en la API de Cohere Chat v2 con el modelo command-r7b-12-2024.

## 2. Herramientas y fuentes usadas

| Herramienta o fuente | Modelo/versión, si se conoce | Finalidad | ¿Se incorporó código o texto? |
|Asistente Antigravity | Gemini 3.8 Flash |Consulta de arquitectura de la API Cohere, estructura JSON de petición y depuración del prompt anti-alucinaciones| llm.py |

## 3. Registro cronológico de uso RELEVANTE de IA y recursos externos

> Repetid la ficha por cada interacción sustantiva: explicación de errores, generación/adaptación de fragmentos, revisión de código, ayuda con pruebas, diseño del prompt, etc. No basta enumerar herramientas. Se puede enlazar una conversación o captura depurada, pero debe existir un **resumen propio** de lo ocurrido.

### Interacción 1 — [fecha/hora aproximada y tarea]

- **Qué intentaba resolver:** Conectar Flask con la API de Cohere Chat v2 mediante llamadas seguras con la librería `requests`, autenticar mediante la clave de entorno `COHERE_API_KEY` y controlar tiempos de espera y códigos de error (401 de credenciales y 429 de límite de cuota).
- **Herramienta/fuente y prompt o instrucción:** Antigravity (Gemini). Le pedí que me explicara cómo enviar la petición HTTP a Cohere v2 en Python, qué formato JSON requiere el cuerpo y cómo gestionar excepciones de timeout sin filtrar la API Key.
- **Qué propuso o respondió:** Sugirió la URL `https://api.cohere.com/v2/chat`, cabeceras `Authorization: Bearer <KEY>`, payload con lista de `messages` con roles (`user`), y bloque `try/except` capturando `requests.exceptions.Timeout` y `RequestException`.
- **Qué hice yo con ello:** Lo incorporé a la función `generar_itinerario` en `web/app/llm.py`, validé previamente que `LLM_MODE == 'cohere'` y añadí el timeout de 20 segundos para evitar bloqueos del servicio web.
- **Resultado y verificación:** Se configuró `.env` con la API key real y se verificó que la respuesta HTTP 200 devuelve el texto en la ruta esperada del JSON.
- **Evidencia:** Archivo `web/app/llm.py` y PR #3 en GitHub.

### Interacción 2 — [duplicar si procede]

- **Qué intentaba resolver:** Comprobar cómo reacciona el LLM cuando la fuente de datos (OpenStreetMap) devuelve muy pocos lugares reales (caso límite: solo 1 lugar disponible).
- **Herramienta/fuente y prompt:** Ejecuté la prueba en Docker pasando únicamente `{'nombre': 'Catedral de Valencia'}` con el prompt inicial V1.
- **Qué propuso o respondió el modelo:** El modelo respondió inventándose 3 sitios adicionales (*Plaza de la Virgen*, *Museo de las Artes y las Ciencias*, *Jardines del Turia*) para cumplir la instrucción de "3 a 5 paradas", y catalogó erróneamente 20 °C como "calor extremo".
- **Qué hice yo con ello:** Consulté con la IA cómo resolver este conflicto. Decidí implementar en Python una lógica de prompt dinámico en `_construir_prompt`: si `len(lugares) < 3`, se inyecta una regla estricta que prohíbe añadir nuevos sitios y obliga al modelo a advertir que los datos son insuficientes.
- **Resultado y verificación:** Al repetir la prueba en Docker con la Versión 2 del prompt, Cohere emitió el aviso explícito de falta de datos y describió únicamente la Catedral de Valencia, eliminando el 100% de las alucinaciones.
- **Evidencia:** Registro de salida en terminal PowerShell, commit `ff32afb` y PR #3.

## 4. Evolución del prompt de itinerarios (si utilizaste el LLM)

- **Objetivo de mi prompt:** Instruir a Cohere para que organice un recorrido urbano lógico adaptado al clima y preferencias, utilizando **únicamente** los lugares verificados de la lista, con prohibición explícita de inventar sitios y obligación de avisar si los datos son insuficientes.

- **Versión inicial V1:**
```text
Eres CityPilot, un asistente experto en planificación de rutas urbanas.
Tu objetivo es diseñar una propuesta de itinerario turístico coherente y realista basada EXCLUSIVAMENTE en datos verificados.
DATOS DE LA SOLICITUD:
- Ciudad: {ciudad} | Tipo: {tipo} | Tiempo disponible: {duracion} horas | Preferencias: {preferencias}
- Clima actual: {temp} °C, precipitación: {precip} mm
LUGARES REALES VERIFICADOS DISPONIBLES:
{lista_lugares_str}
REGLAS ESTRICTAS QUE DEBES CUMPLIR:
1. SELECCIÓN DE LUGARES: Escoge entre 3 y 5 paradas ÚNICAMENTE del listado de 'LUGARES REALES VERIFICADOS DISPONIBLES'.
2. PROHIBIDO ALUCINAR: No inventes nombres de lugares, museos, monumentos, calles ni horarios que no estén en la lista. Si la lista está vacía o tiene menos de 2 sitios, indícalo expresamente y no crees una ruta inventada.
3. ADAPTACIÓN AL CLIMA: Justifica las paradas en función del clima actual.
4. FORMATO DE RESPUESTA: Resumen climático, paradas seleccionadas, consejos.
```

- **Prueba realizada:**
  - Petición para Valencia, 4 horas, cultural, 20 °C sin lluvia.
  - Lista de entrada forzada con solo 1 lugar: `[{'nombre': 'Catedral de Valencia', 'categoria': 'monument'}]`.

- **Problema identificado (Alucinación):**
  La instrucción generó un conflicto en el modelo: por un lado se prohibía alucinar, pero por otro se le exigían "entre 3 y 5 paradas". El modelo priorizó satisfacer el número de paradas y alucinó inventándose tres lugares inexistentes en la entrada (*Plaza de la Virgen, Museo de las Artes y las Ciencias, Jardines del Turia*). Además, afirmó que 20 °C era "calor extremo".

- **Cambio introducido / V2:**
  Refactoricé `_construir_prompt` para evaluar mediante código Python la longitud de la lista de lugares (`total_lugares = len(lugares)`). 
  - Si `total_lugares < 3`, se cambia dinámicamente la instrucción del prompt a:
    > *"ALERTA DE DATOS INSUFICIENTES: Solo dispones de {total_lugares} lugar(es) real(es). ESTÁ TERMINANTEMENTE PROHIBIDO inventar monumentos, plazas o calles para rellenar el tiempo. Debes advertir claramente al usuario: 'Aviso: No hay suficientes lugares verificados en la base de datos para completar un itinerario de {duracion} horas'. Comenta y organiza únicamente los lugares disponibles."*
  - Se calibró la regla climática para que reconozca 20 °C como temperatura templada.

- **Comprobación final:**
  Repetición de la prueba en Docker con el prompt V2. Respuesta obtenida del modelo:
  > *"Aviso: no hay suficientes lugares verificados disponibles en la base de datos para una ruta completa de 4 horas. La única opción disponible es la Catedral de Valencia, un monumento impresionante que merece una visita."*
  Se demostró la eliminación total de la alucinación y el cumplimiento estricto del contrato de negocio.
  
## 5. Código o materiales externos incorporados

| Archivo/líneas aproximadas | Origen (IA, documentación, GitHub, compañero...) | ¿Copiado o adaptado? | ¿Qué cambio/validación hice? |
|---|---|---|---|
| `web/app/llm.py` | Documentación Cohere v2 y asistencia de Antigravity | Adaptado | Estructuré el payload para Chat v2, añadí gestión de cabeceras seguras mediante variables de entorno, control de timeouts y códigos HTTP 401/429. |

## 6. Balance personal

- **Dos decisiones técnicas que tomé yo:** 
  1. **Generación dinámica del prompt en Python:** Comprobar el volumen de datos verificados antes de enviar la instrucción al LLM, adaptando las reglas según si hay suficientes sitios o no para evitar contradicciones lógicas en el modelo.
  2. **Aislamiento de credenciales y resiliencia:** Mantener la `COHERE_API_KEY` estrictamente en el entorno del contenedor sin exponerla en logs, implementando timeouts de red y soportando el modo de contingencia `LLM_MODE=mock`.
- **Un error o solución que descarté:** 
  Descarté usar un único prompt rígido que pretendiera cubrir todos los casos a base de texto estático, ya que las pruebas demostraron que los LLMs tienden a priorizar rellenar el formato de respuesta por encima de restricciones negativas genera.

- **Qué código puedo explicar y demostrar:** 
  Todo el contenido de `web/app/llm.py`, la llamada HTTP a la API de Cohere, el tratamiento del JSON de respuesta.
- **Qué sigue pendiente o limitado:** 

**Declaración:** Confirmo que la memoria describe fielmente mis fuentes, la asistencia recibida, los cambios que introduje y mi aportación personal.