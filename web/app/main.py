"""Rutas HTTP del servicio Flask."""
from io import BytesIO

import matplotlib

matplotlib.use("Agg")

from flask import Flask, jsonify, render_template, request, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from requests import RequestException
from sqlalchemy.exc import SQLAlchemyError

from app.db import (
    obtener_estadisticas,
    obtener_ultimas_solicitudes,
    ping_db,
)
from app.orchestrator import DURACIONES_VALIDAS, TIPOS_VALIDOS, procesar_solicitud


def _validar_entrada(datos: dict, nombres: dict[str, str]) -> tuple[dict | None, str | None]:
    """Normaliza y valida los campos compartidos por el formulario y la API."""
    ciudad = datos.get(nombres["ciudad"])
    tipo = datos.get(nombres["tipo"])
    duracion = datos.get(nombres["duracion"])
    preferencias = datos.get(nombres["preferencias"], "")

    if not isinstance(ciudad, str) or not ciudad.strip():
        return None, "Indica una ciudad."
    ciudad = ciudad.strip()
    if len(ciudad) > 60:
        return None, "La ciudad no puede superar los 60 caracteres."

    if not isinstance(tipo, str) or tipo.strip().lower() not in TIPOS_VALIDOS:
        return None, "Selecciona un tipo de turismo válido."
    tipo = tipo.strip().lower()

    if isinstance(duracion, bool):
        return None, "La duración debe ser de 2, 4 o 6 horas."
    if isinstance(duracion, str):
        duracion = duracion.strip()
        if not duracion.isdigit():
            return None, "La duración debe ser de 2, 4 o 6 horas."
        duracion = int(duracion)
    elif not isinstance(duracion, int):
        return None, "La duración debe ser de 2, 4 o 6 horas."
    if duracion not in DURACIONES_VALIDAS:
        return None, "La duración debe ser de 2, 4 o 6 horas."

    if not isinstance(preferencias, str):
        return None, "Las preferencias deben ser texto."
    preferencias = preferencias.strip()
    if len(preferencias) > 200:
        return None, "Las preferencias no pueden superar los 200 caracteres."

    return {
        "ciudad": ciudad,
        "tipo_turismo": tipo,
        "duracion_horas": duracion,
        "preferencias": preferencias,
    }, None


def _recibir_entrada_api() -> tuple[dict | None, str | None]:
    if not request.is_json:
        return None, "Envía el contenido como application/json."
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return None, "El cuerpo debe ser un objeto JSON válido."
    return _validar_entrada(
        datos,
        {
            "ciudad": "ciudad",
            "tipo": "tipo_turismo",
            "duracion": "duracion_horas",
            "preferencias": "preferencias",
        },
    )


def _estadisticas():
    """Consulta las métricas y registros recientes desde PostgreSQL."""
    resumen = obtener_estadisticas()
    ultimas = obtener_ultimas_solicitudes(limite=8)
    return resumen, ultimas


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def inicio():
        return render_template("index.html", valores={})

    @app.get("/api/health")
    def health():
        try:
            ping_db()
            return jsonify(servicio="citypilot", estado="ok", db="ok")
        except Exception:
            app.logger.exception("No se pudo comprobar la conexión con PostgreSQL")
            return jsonify(servicio="citypilot", estado="degradado", db="error"), 503

    @app.post("/planificar")
    def planificar_html():
        datos, error = _validar_entrada(
            request.form,
            {
                "ciudad": "Ciudad",
                "tipo": "Tipo",
                "duracion": "Duracion",
                "preferencias": "Preferencias",
            },
        )
        valores = {
            "Tipo": request.form.get("Tipo", ""),
            "Duracion": request.form.get("Duracion", ""),
        }
        if error:
            return render_template("index.html", valores=valores, error=error), 400

        try:
            resultado = procesar_solicitud(**datos)
        except ValueError as exc:
            return render_template("index.html", valores=valores, error=str(exc)), 400
        except NotImplementedError:
            app.logger.exception("El flujo de planificación no está implementado")
            return (
                render_template(
                    "index.html",
                    valores=valores,
                    error="El servicio de planificación todavía no está disponible.",
                ),
                501,
            )
        except RequestException:
            app.logger.exception("Falló una consulta a un proveedor externo")
            return (
                render_template(
                    "index.html",
                    valores=valores,
                    error="No se pudo consultar un proveedor externo. Inténtalo de nuevo más tarde.",
                ),
                502,
            )
        except RuntimeError:
            app.logger.exception("El servicio de planificación no está configurado")
            return (
                render_template(
                    "index.html",
                    valores=valores,
                    error="El servicio de planificación no está disponible por configuración.",
                ),
                503,
            )

        return render_template("resultado.html", resultado=resultado)

    @app.post("/api/planificar")
    def planificar_api():
        datos, error = _recibir_entrada_api()
        if error:
            return jsonify(error=error), 400

        try:
            resultado = procesar_solicitud(**datos)
        except ValueError as exc:
            return jsonify(error=str(exc)), 400
        except NotImplementedError:
            app.logger.exception("El flujo de planificación no está implementado")
            return jsonify(error="El servicio de planificación todavía no está disponible."), 501
        except RequestException:
            app.logger.exception("Falló una consulta a un proveedor externo")
            return jsonify(error="No se pudo consultar un proveedor externo."), 502
        except RuntimeError:
            app.logger.exception("El servicio de planificación no está configurado")
            return jsonify(error="El servicio de planificación no está disponible."), 503

        return jsonify(resultado)

    @app.get("/analitica")
    def analitica():
        try:
            resumen, ultimas = _estadisticas()
        except NotImplementedError:
            app.logger.exception("Las consultas de analítica no están implementadas")
            return "La analítica todavía no está disponible.", 501
        except (SQLAlchemyError, RuntimeError):
            app.logger.exception("No se pudieron consultar las métricas de PostgreSQL")
            return "No se pudo cargar la analítica en este momento.", 503

        return render_template(
            "analitica.html",
            totales=resumen,
            top_ciudades=resumen.get("por_ciudad", []),
            ultimas=ultimas,
        )

    @app.get("/analitica/grafico.png")
    def grafico():
        try:
            resumen = obtener_estadisticas()
        except NotImplementedError:
            app.logger.exception("La consulta para el gráfico no está implementada")
            return "El gráfico todavía no está disponible.", 501
        except (SQLAlchemyError, RuntimeError):
            app.logger.exception("No se pudieron consultar los datos del gráfico")
            return "No se pudo generar el gráfico en este momento.", 503

        ciudades = resumen.get("por_ciudad", [])
        nombres = [fila["ciudad"] for fila in ciudades]
        cantidades = [fila["total"] for fila in ciudades]

        figura = Figure(figsize=(8, 4.5), constrained_layout=True)
        eje = figura.subplots()
        if nombres:
            eje.bar(nombres, cantidades, color="#4857d5", width=.65)
            eje.set_ylabel("Solicitudes")
            eje.tick_params(axis="x", rotation=25)
        else:
            eje.text(.5, .5, "Todavía no hay solicitudes", ha="center", va="center")
            eje.set_axis_off()
        eje.set_title("Solicitudes por ciudad")
        eje.spines[["top", "right"]].set_visible(False)

        imagen = BytesIO()
        FigureCanvasAgg(figura).print_png(imagen)
        imagen.seek(0)
        return send_file(imagen, mimetype="image/png", download_name="solicitudes.png")

    @app.get("/api/estadisticas")
    def estadisticas_api():
        try:
            resumen, ultimas = _estadisticas()
        except NotImplementedError:
            app.logger.exception("Las consultas de analítica no están implementadas")
            return jsonify(error="La analítica todavía no está disponible."), 501
        except (SQLAlchemyError, RuntimeError):
            app.logger.exception("No se pudieron consultar las métricas de PostgreSQL")
            return jsonify(error="No se pudo consultar la analítica."), 503

        return jsonify({**resumen, "ultimas": ultimas})

    return app


app = create_app()
