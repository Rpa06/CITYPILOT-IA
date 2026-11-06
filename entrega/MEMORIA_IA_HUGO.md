# Memoria individual de utilización de IA — CityPilot IA

## 1. Autoría y aportación individual

- **Estudiante:** HUGO BALLESTEROS
- **Equipo:** Rafael Pontes, Cristofer Carceller y Darwin Chavez
- **Repositorio:** [Rpa06/CITYPILOT-IA](https://github.com/Rpa06/CITYPILOT-IA)
- **PR indicada en el borrador:** [#4](https://github.com/Rpa06/CITYPILOT-IA/pull/4). La referencia de una segunda PR no estaba incluida en la información disponible.
- **Aportación personal declarada:** desarrollo de HTML y Flask y adición de la imagen de fondo. En el historial del repositorio aparecen cambios del formulario, del estilo y del servidor en los commits [bb2c462](https://github.com/Rpa06/CITYPILOT-IA/commit/bb2c462), [0dbd170](https://github.com/Rpa06/CITYPILOT-IA/commit/0dbd170) y [44fdd56](https://github.com/Rpa06/CITYPILOT-IA/commit/44fdd56).
- **Asistencia recibida en esta conversación:** generación y adaptación de CSS y HTML para la página de planificación y las tarjetas de beneficios; implementación de rutas y validación de entradas en [main.py](../web/app/main.py); y redacción de esta memoria. Estos cambios deben distinguirse de la aportación personal y revisarse antes de defenderlos como propios.
- **Pruebas personales:** no consta que el estudiante haya repetido personalmente las comprobaciones descritas abajo. No se afirma que se haya validado visualmente el sitio en un navegador.

## 2. Herramientas y fuentes usadas

| Herramienta o fuente | Modelo/versión, si se conoce | Finalidad | ¿Se incorporó código o texto? |
|---|---|---|---|
| Copilot en VS Code | Copilot SDK; modelo concreto no indicado | Asistencia de diseño, cambios de HTML/CSS y Flask, validación acotada y apoyo para completar esta memoria | Sí. Se incorporaron fragmentos sustanciales de CSS, HTML y código de rutas, que requieren revisión y explicación por parte del estudiante. |
| ChatGPT | Versión no indicada; uso declarado en el borrador original | Corrección, creación de código y apoyo para esta memoria | Sí, según la declaración original. No se aportó un registro de prompts o cambios concretos de esa herramienta. |
| Git y pruebas con Docker | Versiones no registradas aquí | Consultar historial y comprobar algunas respuestas de las rutas Flask | No se incorporó código de estas herramientas. |

No se documentó en esta memoria una consulta concreta a documentación externa ni se copiaron fragmentos de una fuente externa.

## 3. Registro cronológico de uso relevante de IA

Las fechas siguientes son aproximadas y corresponden a las interacciones registradas en esta conversación, el 6 de noviembre de 2026.

### Interacción 1 — Aproximadamente 10:00: mejora visual del planificador

- **Qué intentaba resolver:** mejorar el aspecto de la página de planificación usando la hoja `static` existente, sin que el resultado pareciera descuidado.
- **Herramienta e instrucción:** Copilot en VS Code recibió la petición «Genera un estilo teniendo en cuenta el static que tenemos pero que no se vea horrible».
- **Qué propuso:** conservar la paleta índigo, reorganizar el CSS, mejorar espaciado, tipografía, controles, foco accesible y adaptación móvil. También observó un cierre de sección sobrante en la plantilla.
- **Qué se incorporó:** cambios en [style.css](../web/app/static/style.css) y [index.html](../web/app/templates/index.html), incluidos el agrupamiento de campos, etiquetas y textos del formulario.
- **Resultado y verificación:** `git diff --check` no detectó errores de whitespace. No se ejecutó una prueba visual en navegador; la primera ejecución local de pytest no pudo iniciarse porque Python no estaba disponible mediante el comando del entorno.
- **Evidencia:** commits [0dbd170](https://github.com/Rpa06/CITYPILOT-IA/commit/0dbd170) y [44fdd56](https://github.com/Rpa06/CITYPILOT-IA/commit/44fdd56), y archivos indicados arriba.

### Interacción 2 — Aproximadamente 10:15: rediseño de beneficios

- **Qué intentaba resolver:** mejorar específicamente las tres tarjetas de meteorología, lugares reales y planificación inteligente.
- **Herramienta e instrucción:** Copilot recibió el bloque seleccionado de `index.html` y la petición de trabajar también en el `main` si fuese necesario.
- **Qué propuso:** transformar las tarjetas en una sección con encabezado, iconos decorativos, descripciones y una cuadrícula de tres columnas que pasa a una columna en pantallas estrechas.
- **Qué se incorporó:** nuevos elementos semánticos en `web/app/templates/index.html` y reglas `.benefits-*` en `web/app/static/style.css`. No fue necesario modificar el `<main>` de `base.html`.
- **Resultado y verificación:** `git diff --check` pasó. No se hizo comprobación visual en navegador.
- **Evidencia:** [index.html](../web/app/templates/index.html), [style.css](../web/app/static/style.css) y el commit [44fdd56](https://github.com/Rpa06/CITYPILOT-IA/commit/44fdd56).

### Interacción 3 — Aproximadamente 10:18: completar las rutas Flask

- **Qué intentaba resolver:** completar [main.py](../web/app/main.py), que contenía rutas pendientes.
- **Herramienta e instrucción:** Copilot recibió la petición «Rellena el main.py». Para seguir los contratos se revisaron el orquestador, los clientes API, la base de datos, la plantilla de resultado, el SQL de inicialización y la documentación del proyecto.
- **Qué se propuso e incorporó:** validación común de los datos del formulario y JSON; uso de `procesar_solicitud` para ambas interfaces; respuestas HTTP controladas; consulta de estadísticas y creación de una imagen PNG en memoria para el gráfico. Se agregó también un aviso de error a la página del formulario.
- **Resultado y verificación:** se construyó la imagen Docker del servicio web. Dentro del contenedor se hicieron comprobaciones acotadas con el cliente de pruebas de Flask: una entrada inválida devuelve 400; con el orquestador sustituido por un stub, una solicitud válida devuelve 200; el endpoint de estadísticas devuelve 200 con funciones de base de datos simuladas; y el endpoint del gráfico devuelve `image/png`. También se verificó el error de ciudad vacía en el formulario. No se ejecutó la suite completa ni se probó la integración real con proveedores o PostgreSQL.
- **Limitaciones:** el resultado de planificación se probó con el orquestador simulado, no con el flujo real. [orchestrator.py](../web/app/orchestrator.py), varias funciones de [db.py](../web/app/db.py), [api_clients.py](../web/app/api_clients.py) y el modo Cohere de [llm.py](../web/app/llm.py) continúan teniendo implementaciones pendientes. La plantilla de analítica también conserva contenido provisional.
- **Evidencia:** [main.py](../web/app/main.py), [index.html](../web/app/templates/index.html), [orchestrator.py](../web/app/orchestrator.py), [db.py](../web/app/db.py) y el commit [44fdd56](https://github.com/Rpa06/CITYPILOT-IA/commit/44fdd56).

### Interacción 4 — Aproximadamente 10:53: redacción de esta memoria

- **Qué intentaba resolver:** completar `entrega/MEMORIA_IA_HUGO.md` a partir del borrador existente y del trabajo registrado.
- **Herramienta e instrucción:** Copilot recibió la petición «Rellena la memoria de la IA».
- **Qué se propuso:** documentar las interacciones, los cambios asistidos y las pruebas efectivamente ejecutadas, sin afirmar que se probó el sitio completo ni que se implementó el modelo generativo.
- **Qué hice con ello:** incorporé esta información en el archivo de memoria, conservando el equipo y las aportaciones personales tal como estaban declaradas en el borrador y distinguiéndolas del trabajo asistido.
- **Resultado y verificación:** pendiente de revisión personal de la exactitud de la declaración, especialmente de las aportaciones, PR y pruebas que el estudiante ejecutó por su cuenta.
- **Evidencia:** [esta memoria](./MEMORIA_IA_HUGO.md).

## 4. Evolución del prompt de itinerarios

- **Estado:** no se diseñó ni se probó un prompt propio de itinerarios en las interacciones documentadas aquí.
- **V1, pruebas y V2:** no disponibles. No se deben inventar resultados de experimentos ni atribuirse una evaluación de alucinaciones.
- **Motivo:** [llm.py](../web/app/llm.py) sigue pendiente en el modo Cohere. Su modo `mock` devuelve texto de simulación, no es una llamada generativa y no demuestra el cumplimiento de las restricciones del prompt.
- **Trabajo necesario:** redactar y probar un prompt que utilice únicamente lugares recibidos, tenga en cuenta meteorología, duración y preferencias, y comunique con claridad la falta de datos o el uso de datos demo. Documentar ejemplos reales sin claves ni información sensible.

## 5. Código o materiales externos incorporados

| Archivo/líneas aproximadas | Origen | ¿Copiado o adaptado? | Cambio o validación |
|---|---|---|---|
| [style.css](../web/app/static/style.css) | Asistencia de Copilot y estilo existente del proyecto | CSS nuevo y adaptado a la paleta, clases y estructura existentes | `git diff --check`; falta inspección visual en navegador. |
| [index.html](../web/app/templates/index.html) | Asistencia de Copilot y formulario existente | Se reorganizó el formulario y se creó la sección de beneficios; se conserva Jinja | `git diff --check`; falta prueba visual. |
| [main.py](../web/app/main.py) | Asistencia de Copilot y contratos en [APIS_Y_CONTRATOS.md](../docs/APIS_Y_CONTRATOS.md) | Se completaron rutas, validación, manejo de respuestas y generación de gráfico | Comprobaciones de rutas con Flask en Docker usando stubs; no prueba de integración real. |
| [MEMORIA_IA_HUGO.md](./MEMORIA_IA_HUGO.md) | Asistencia de Copilot y datos del borrador original | Redacción y organización de la memoria | El estudiante debe verificar que la declaración personal sea fiel antes de entregarla. |

No se registraron claves, tokens ni credenciales en el código o en esta memoria. No se incorporó código de una API o repositorio externo.

## 6. Balance personal

- **Decisiones y criterios técnicos reflejados en el trabajo:** reutilizar la paleta y estructura Jinja del proyecto en lugar de introducir otro framework; y compartir la función de procesamiento entre el formulario y la API para evitar duplicar el flujo. La implementación de estas decisiones recibió asistencia de Copilot.
- **Problema o enfoque descartado:** la primera ejecución de pytest no funcionó porque el ejecutable `python` del entorno Windows apuntaba al alias de Microsoft Store y no a una instalación disponible. Se usó el contenedor Docker del proyecto para hacer comprobaciones acotadas; esto no sustituye la suite completa ni la validación del flujo real.
- **Código que debo poder explicar y demostrar:** estructura Jinja y clases visuales del formulario y beneficios; validación y códigos HTTP de `main.py`; diferencia entre datos reales y demo; y responsabilidades del orquestador, clientes externos y persistencia.
- **Pendiente o limitado:** repetir las pruebas personalmente; comprobar la interfaz en navegador y distintos tamaños; implementar y probar la integración real de [orchestrator.py](../web/app/orchestrator.py), [api_clients.py](../web/app/api_clients.py) y [db.py](../web/app/db.py); terminar el cliente Cohere y documentar su prompt; completar las plantillas y analítica; confirmar la referencia de la segunda PR.

**Declaración:** esta memoria distingue la aportación personal declarada de la asistencia de IA registrada. Antes de entregarla, debo revisar que los datos personales, las PR, las pruebas y la descripción de mi trabajo sean exactos y cambiar cualquier afirmación que no pueda demostrar.

**Nombre:** HUGO BALLESTEROS  
**Fecha de revisión y firma:** pendiente de completar personalmente.
