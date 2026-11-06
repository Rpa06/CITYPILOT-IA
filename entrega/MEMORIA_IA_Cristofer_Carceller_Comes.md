# Memoria individual de utilización de IA — CityPilot IA

> **Rellenad una copia de este documento POR PERSONA** y guardadla como `entrega/MEMORIA_IA_<NOMBRE>.md`. Actividad de **semáforo amarillo**. Puede utilizarse IA como asistencia, pero debe quedar documentada con precisión. No incluyáis secretos. Si no habéis usado IA, decidlo expresamente y justificad el trabajo propio con evidencias.

## 1. Autoría y aportación individual

- Estudiante: Cristofer Carceller Comes
- Equipo: Darwin, Rafael, Hugo
- Repositorio GitHub: https://github.com/Rpa06/CITYPILOT-IA
- Mis dos PR, con revisión cruzada: [implementar la capa de persistencia PostgreSQL] y [Implementar orquestación del flujo de planificación]
- Archivos o funciones que implementé personalmente: definí el alcance y pedí ajustes concretos para `web/app/db.py` y `web/app/orchestrator.py`. Partes del código fueron generadas con asistencia de IA.
- Pruebas que ejecuté personalmente y resultado: no ejecuté personalmente las pruebas. Durante la asistencia se ejecutaron cuatro pruebas simuladas de DB (pasaron) y una comprobación simulada del orquestador (flujo válido con ID 42 y ciudad vacía con HTTP 400).

## 2. Herramientas y fuentes usadas

| Herramienta o fuente | Modelo/versión, si se conoce | Finalidad | ¿Se incorporó código o texto? |
|---|---|---|---|
| Asistente de IA de VS Code | Modelo específico no visible | Ayuda con persistencia, orquestación y comprobaciones | Sí, partes de `web/app/db.py` y `web/app/orchestrator.py` |

## 3. Registro cronológico de uso RELEVANTE de IA y recursos externos

### Interacción 1 — 6 de noviembre de 2026, 09:22–09:50 — Persistencia PostgreSQL

- **Qué intentaba resolver:** campos JSONB, estadísticas y últimas solicitudes para PR1.
- **Herramienta/fuente y prompt o instrucción:** asistente de IA de VS Code; pedí implementar las funciones DB según los contratos.
- **Qué propuso o respondió:** generó parte del código de la implementación de `obtener_estadisticas` y `obtener_ultimas_solicitudes`, además de pruebas simuladas.
- **Qué hice yo con ello:** Utilizarlo
- **Resultado y verificación:** las cuatro pruebas simuladas pasaron.
- **Evidencia:** `web/app/db.py`, commit `796e8b9`, rama `feat/postgresdb`.

### Interacción 2 — 6 de noviembre de 2026, 10:30–10:40 — Orquestador

- **Qué intentaba resolver:** corregir el flujo de `web/app/orchestrator.py` para validar, integrar proveedores, generar el itinerario y guardar la solicitud.
- **Herramienta/fuente y prompt:** asistente de IA de VS Code; pedí corregir el archivo existente sin añadir código nuevo.
- **Qué propuso:** validación de entradas, contexto en forma de diccionario, llamadas a geocodificación, meteorología, lugares y LLM, guardado parametrizado y respuesta común.
- **Qué hice yo:** indiqué mantener las herramientas ya implementadas por Rafael y revisé el resultado. El código se guardó en el commit `d1d7070`.
- **Resultado y verificación:** en el contenedor se probó con servicios simulados; el flujo válido devolvió ID 42 y la ciudad vacía respondió HTTP 400. No se comprobaron servicios externos ni una escritura real en DB.
- **Evidencia:** `web/app/orchestrator.py`, commit `d1d7070`, rama `feat/orchestator`.

## 4. Evolución del prompt de itinerarios (si utilizaste el LLM)

- **Objetivo de mi prompt:** no diseñé un prompt propio.
- **Versión inicial V1:** no aplica; no modifiqué el prompt de `web/app/llm.py`.
- **Prueba realizada:** no realicé pruebas del prompt ni con Cohere.
- **Problema identificado:** no evaluado.
- **Cambio introducido / V2:** ninguno.
- **Comprobación final:** no aplica.

## 5. Código o materiales externos incorporados

| Archivo/líneas aproximadas | Origen (IA, documentación, GitHub, compañero...) | ¿Copiado o adaptado? | ¿Qué cambio/validación hice? |
|---|---|---|---|
| `web/app/db.py` (`obtener_estadisticas`, `obtener_ultimas_solicitudes`) | Asistente de IA de VS Code | Parte del código fue generado con asistencia; pedí utilizarlo | Se ejecutaron cuatro pruebas simuladas y pasaron. No las ejecuté personalmente |
| `web/app/orchestrator.py` (`procesar_solicitud`) | Asistente de IA de VS Code; herramientas existentes implementadas por Rafael | Código generado con asistencia para coordinar esas herramientas | Se comprobó con datos simulados: el flujo válido devolvió ID 42 y la ciudad vacía respondió HTTP 400. No ejecuté personalmente la prueba |

## 6. Balance personal

- **Dos decisiones técnicas que tomé yo:** centrar el trabajo en persistencia y orquestación, y en el orquestador reutilizar las herramientas que ya había implementado Rafael en vez de añadir otras.
- **Un error o solución que descarté:** no se describe un error concreto descartado en los puntos anteriores. Las pruebas disponibles fueron simuladas, no de integración real.
- **Qué código puedo explicar y demostrar:** puedo explicar qué funciones de persistencia se solicitaron y cómo el orquestador coordina la validación, los proveedores, el LLM y el guardado. En la comprobación simulada, el flujo válido devolvió ID 42 y una ciudad vacía respondió HTTP 400.
- **Qué sigue pendiente o limitado:** no se probaron proveedores reales ni una escritura real en DB; tampoco diseñé ni probé el prompt de Cohere.

**Declaración:** Confirmo que esta memoria describe mi uso de IA y las comprobaciones realizadas, sin atribuirme como propio el código generado por el asistente. Cristofer Carceller Comes / 6 de noviembre de 2026
