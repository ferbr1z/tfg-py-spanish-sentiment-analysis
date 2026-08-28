"""
Seeder de Topics/SubTopics desde un CSV de dos columnas: topic, subtopic.

Uso:
    python -m database.seed_topics                            # usa database/wordlist.csv
    python -m database.seed_topics wordlist1.csv              # busca dentro de database/
    python -m database.seed_topics ruta/al/archivo.csv
    python -m database.seed_topics ruta/al/archivo.csv --no-header
"""
import argparse
import asyncio
import sys
from pathlib import Path

import pandas as pd
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from database.connection import create_db_and_tables, dispose_engine, session_context
from database.models import SubTopic, Topic


DEFAULT_CSV = Path(__file__).resolve().parent / "wordlist.csv"


def resolve_csv_path(csv_path: Path) -> Path:
    """Resuelve nombres simples de CSV con respecto al directorio database/."""
    if csv_path.is_file() or csv_path.is_absolute():
        return csv_path

    database_csv_path = DEFAULT_CSV.parent / csv_path
    return database_csv_path if database_csv_path.is_file() else csv_path


def read_pairs(csv_path: Path, *, has_header: bool = True, delimiter: str = ",") -> pd.DataFrame:
    """Lee los pares (topic, subtopic) del CSV usando las dos primeras columnas."""
    df = pd.read_csv(
        csv_path,
        header=0 if has_header else None,
        sep=delimiter,
        usecols=[0, 1],
        dtype=str,
    )
    df.columns = ["topic", "subtopic"]

    df["topic"] = df["topic"].str.strip()
    df["subtopic"] = df["subtopic"].str.strip()
    df = df.replace("", pd.NA).dropna().drop_duplicates()

    return df.reset_index(drop=True)


async def get_or_create_topic(session: AsyncSession, name: str, cache: dict[str, Topic]) -> Topic:
    """Devuelve el Topic con ese nombre (el primero si esta repetido), creandolo si no existe."""
    if name in cache:
        return cache[name]

    topic = (await session.exec(select(Topic).where(Topic.name == name))).first()

    if topic is None:
        topic = Topic(name=name)
        session.add(topic)
        await session.flush()

    cache[name] = topic
    return topic


async def seed_from_csv(csv_path: Path, *, has_header: bool = True, delimiter: str = ",") -> None:
    pairs = read_pairs(csv_path, has_header=has_header, delimiter=delimiter)

    topics: dict[str, Topic] = {}
    new_subtopics = 0

    await create_db_and_tables()

    async with session_context() as session:
        for row in pairs.itertuples(index=False):
            topic = await get_or_create_topic(session, row.topic, topics)

            statement = select(SubTopic).where(
                SubTopic.name == row.subtopic,
                SubTopic.topic_id == topic.id,
            )
            if (await session.exec(statement)).first() is not None:
                continue

            session.add(SubTopic(name=row.subtopic, topic_id=topic.id))
            new_subtopics += 1

    print(
        f"{len(pairs)} pares leidos desde {csv_path}: "
        f"{len(topics)} topics procesados, {new_subtopics} subtopics nuevos"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga Topics y SubTopics desde un CSV.")
    parser.add_argument("csv_path", type=Path, nargs="?", default=DEFAULT_CSV, help="Ruta al CSV con columnas topic,subtopic")
    parser.add_argument("--no-header", action="store_true", help="El CSV no tiene fila de encabezado")
    parser.add_argument("--delimiter", default=",", help="Separador de columnas (por defecto ',')")
    args = parser.parse_args()

    csv_path = resolve_csv_path(args.csv_path)
    if not csv_path.is_file():
        parser.error(f"No existe el archivo: {args.csv_path}")

    async def run() -> None:
        try:
            await seed_from_csv(
                csv_path,
                has_header=not args.no_header,
                delimiter=args.delimiter,
            )
        finally:
            await dispose_engine()

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(run())


if __name__ == "__main__":
    main()
