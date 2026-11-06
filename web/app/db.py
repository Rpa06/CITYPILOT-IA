"""Acceso a PostgreSQL para persistencia y analítica de solicitudes."""
import json
import os

from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL", "")
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None


def _require_engine():
    if engine is None:
        raise RuntimeError("Falta DATABASE_URL")
    return engine


def ping_db():
    with _require_engine().connect() as conn:
        return conn.execute(text("SELECT 1")).scalar_one()


def guardar_solicitud(registro: dict) -> int:
    """Inserta una solicitud y devuelve su identificador."""
    consulta = text(
        """
        INSERT INTO solicitudes (
            ciudad, pais, tipo_turismo, duracion_horas, preferencias,
            latitud, longitud, meteorologia, lugares, prompt_usado,
            itinerario, modo_demo, modo_modelo, estado, duracion_ms,
            error_resumido
        ) VALUES (
            :ciudad, :pais, :tipo_turismo, :duracion_horas, :preferencias,
            :latitud, :longitud, CAST(:meteorologia AS jsonb),
            CAST(:lugares AS jsonb), :prompt_usado,
            :itinerario, :modo_demo, :modo_modelo, :estado, :duracion_ms,
            :error_resumido
        )
        RETURNING id
        """
    )
    valores = {
        "ciudad": registro["ciudad"],
        "pais": registro.get("pais"),
        "tipo_turismo": registro["tipo_turismo"],
        "duracion_horas": registro["duracion_horas"],
        "preferencias": registro.get("preferencias") or "",
        "latitud": registro.get("latitud"),
        "longitud": registro.get("longitud"),
        "meteorologia": json.dumps(
            registro.get("meteorologia") or {}, ensure_ascii=False
        ),
        "lugares": json.dumps(registro.get("lugares") or [], ensure_ascii=False),
        "prompt_usado": registro.get("prompt_usado"),
        "itinerario": registro.get("itinerario"),
        "modo_demo": registro.get("modo_demo", False),
        "modo_modelo": registro.get("modo_modelo"),
        "estado": registro.get("estado") or "pendiente",
        "duracion_ms": registro.get("duracion_ms"),
        "error_resumido": registro.get("error_resumido"),
    }

    with _require_engine().begin() as conn:
        return conn.execute(consulta, valores).scalar_one()


def obtener_estadisticas() -> dict:
    """Devuelve totales y distribuciones de las solicitudes almacenadas."""
    consultas = {
        "resumen": text(
            """
            SELECT COUNT(*) AS total,
                   COUNT(DISTINCT ciudad) AS ciudades_distintas,
                   COUNT(*) FILTER (WHERE estado = 'error') AS errores
            FROM solicitudes
            """
        ),
        "por_ciudad": text(
            """
            SELECT ciudad, COUNT(*) AS solicitudes
            FROM solicitudes
            GROUP BY ciudad
            ORDER BY solicitudes DESC, ciudad
            """
        ),
        "por_tipo": text(
            """
            SELECT tipo_turismo, COUNT(*) AS solicitudes
            FROM solicitudes
            GROUP BY tipo_turismo
            ORDER BY solicitudes DESC, tipo_turismo
            """
        ),
    }

    with _require_engine().connect() as conn:
        resumen = dict(conn.execute(consultas["resumen"]).mappings().one())
        por_ciudad = [
            dict(fila) for fila in conn.execute(consultas["por_ciudad"]).mappings()
        ]
        por_tipo = [
            dict(fila) for fila in conn.execute(consultas["por_tipo"]).mappings()
        ]

    return {**resumen, "por_ciudad": por_ciudad, "por_tipo": por_tipo}


def obtener_ultimas_solicitudes(limite: int = 8) -> list[dict]:
    """Devuelve solicitudes recientes con campos apropiados para el dashboard."""
    if isinstance(limite, bool) or not isinstance(limite, int) or limite < 1:
        raise ValueError("limite debe ser un entero positivo")

    consulta = text(
        """
        SELECT id, fecha, ciudad, tipo_turismo, duracion_horas, estado,
               duracion_ms, modo_demo
        FROM solicitudes
        ORDER BY fecha DESC, id DESC
        LIMIT :limite
        """
    )
    with _require_engine().connect() as conn:
        return [
            dict(fila)
            for fila in conn.execute(consulta, {"limite": limite}).mappings()
        ]
