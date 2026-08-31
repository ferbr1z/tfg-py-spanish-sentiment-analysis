"""Ayudante para inicializar Alembic sobre una base que ya existe con datos.

Uso (desde la raiz del proyecto, con el venv):

    .venv/bin/python -m database.bootstrap_alembic baseline
    # -> crea una DB temporal vacia, autogenera la migracion baseline y la borra.
    #    Revisas el archivo generado en alembic/versions/ ...

    .venv/bin/python -m database.bootstrap_alembic stamp
    # -> marca el baseline como aplicado en la DB REAL (sin ejecutar SQL, datos intactos).

No usa los binarios createdb/dropdb: crea y borra la DB temporal con psycopg,
que ya viene instalado. Conecta con las credenciales de tu .env.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import psycopg

from config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMP_DB = "tfg_baseline"


def _admin_connection() -> psycopg.Connection:
    """Conexion a la DB de mantenimiento 'postgres' en autocommit (para CREATE/DROP DATABASE)."""
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname="postgres",
        autocommit=True,
    )


def _run_alembic(args: list[str], db_name: str | None = None) -> None:
    """Corre alembic como subproceso, opcionalmente pisando DB_NAME (para apuntar a otra DB)."""
    env = None
    if db_name is not None:
        import os

        env = os.environ.copy()
        env["DB_NAME"] = db_name

    subprocess.run(
        [sys.executable, "-c", "from alembic.config import main; main()", *args],
        cwd=PROJECT_ROOT,
        env=env,
        check=True,
    )


def baseline() -> None:
    print(f"[1/3] Creando DB temporal vacia '{TEMP_DB}' ...")
    with _admin_connection() as conn:
        conn.execute(f'DROP DATABASE IF EXISTS "{TEMP_DB}"')
        conn.execute(f'CREATE DATABASE "{TEMP_DB}"')

    try:
        print("[2/3] Autogenerando la migracion baseline contra la DB vacia ...")
        _run_alembic(
            ["revision", "--autogenerate", "-m", "baseline schema"],
            db_name=TEMP_DB,
        )
    finally:
        print(f"[3/3] Borrando DB temporal '{TEMP_DB}' ...")
        with _admin_connection() as conn:
            conn.execute(f'DROP DATABASE IF EXISTS "{TEMP_DB}"')

    print()
    print("Listo. Ahora:")
    print("  1) Revisa el archivo nuevo en alembic/versions/ (enum Lang, DateTime tz, indices, FKs).")
    print("  2) Cuando este ok, registralo en la DB real sin ejecutar SQL:")
    print("       .venv/bin/python -m database.bootstrap_alembic stamp")


def stamp() -> None:
    print("Marcando el baseline como aplicado en la DB real (no ejecuta SQL de esquema) ...")
    _run_alembic(["stamp", "head"])
    print("Hecho. La DB real quedo registrada en el baseline; los datos no se tocaron.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap de Alembic sobre una DB existente.")
    parser.add_argument("command", choices=["baseline", "stamp"])
    args = parser.parse_args()

    if args.command == "baseline":
        baseline()
    elif args.command == "stamp":
        stamp()


if __name__ == "__main__":
    main()
