# Memoria individual de utilización de IA — CityPilot IA

> **Rellenad una copia de este documento POR PERSONA** y guardadla como `entrega/MEMORIA_IA_<NOMBRE>.md`. Actividad de **semáforo amarillo**. Puede utilizarse IA como asistencia, pero debe quedar documentada con precisión. No incluyáis secretos. Si no habéis usado IA, decidlo expresamente y justificad el trabajo propio con evidencias.

## 1. Autoría y aportación individual

- Estudiante: Rafael Pontes Alvarez
- Equipo: Darwin, Cristofer, Hugo
- Repositorio GitHub: https://github.com/Rpa06/CITYPILOT-IA/
- Mis dos PR, con revisión cruzada: https://github.com/Rpa06/CITYPILOT-IA/pull/1 y [PR 2]
- Archivos o funciones que implementé personalmente: api_clientes.py, colabore en orchestator.py
- Pruebas que ejecuté personalmente y resultado: Probe en el jupyter los requests.get

## 2. Herramientas y fuentes usadas

| Herramienta o fuente | Modelo/versión, si se conoce | Finalidad | ¿Se incorporó código o texto? |
|---|---|---|---|
| Gemini | no se | Investigacion, aprendizaje y correccion de errores | Si, secciones complicadas en donde se corrigieron los errores |

- Si no utilicé IA generativa: [escribir «No he utilizado IA generativa», y fuentes que sí consulté].

## 3. Registro cronológico de uso RELEVANTE de IA y recursos externos

> Repetid la ficha por cada interacción sustantiva: explicación de errores, generación/adaptación de fragmentos, revisión de código, ayuda con pruebas, diseño del prompt, etc. No basta enumerar herramientas. Se puede enlazar una conversación o captura depurada, pero debe existir un **resumen propio** de lo ocurrido.

### Interacción 1 — ni idea de fecha y hora, 

- **Qué intentaba resolver:** Aprender a usar la api de overpass
- **Herramienta/fuente y prompt o instrucción:** how to use the overpass api?
- **Qué propuso o respondió:** Ofrecio el codigo que se uso de inspiracion
- **Qué hice yo con ello:** Adapte los valores y metadatos
- **Resultado y verificación:** Probe en postman una URL
- **Evidencia:** api_clients.py

## 4. Evolución del prompt de itinerarios (si utilizaste el LLM)

- **Objetivo de mi prompt:** [qué datos debe interpretar y qué resultado solicitar]
- **Versión inicial V1:** [texto completo del prompt de aplicación o archivo/commit donde figura; su autor debe ser identificable]
- **Prueba realizada:** [datos de ciudad, clima y preferencias; resultado relevante, sin credenciales]
- **Problema identificado:** [alucinación, duración, lluvia, falta de lugares, formato, etc.; si no hubo problema, indicarlo]
- **Cambio introducido / V2:** [qué modificaste y por qué, o motivo por el que mantuviste V1]
- **Comprobación final:** [cómo verificaste que utiliza solo lugares consultados y respeta las preferencias]

## 5. Código o materiales externos incorporados

| Archivo/líneas aproximadas | Origen (IA, documentación, GitHub, compañero...) | ¿Copiado o adaptado? | ¿Qué cambio/validación hice? |
|---|---|---|---|
| [ej. `web/app/api_clients.py` / función] | [link o fuente] | [detalle] | [detalle] |

## 6. Balance personal

- **Dos decisiones técnicas que tomé yo:** 
- **Un error o solución que descarté:** Forze tipado a la respuesta pero esa daba error debido a probabiidad de None
- **Qué código puedo explicar y demostrar:** api_clients.py, orchestator.py
- **Qué sigue pendiente o limitado:** manejo de errores

**Declaración:** Confirmo que la memoria describe fielmente mis fuentes, la asistencia recibida, los cambios que introduje y mi aportación personal. [nombre / fecha]
