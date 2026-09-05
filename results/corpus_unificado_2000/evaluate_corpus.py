from __future__ import annotations

import argparse
import random
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
CORPUS_PATH = BASE_DIR / "corpus_unificado_2000.csv"
OUTPUT_COLUMNS = ["id", "identifier", "text", "sentimiento_humano", "ironia_humana"]
SENTIMENTS = ["NEG", "NEU", "POS"]
SENTIMENT_TARGETS = {"NEG": 33, "NEU": 34, "POS": 33}


def load_corpus(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    required = {"id", "identifier", "text", "categoria", "sentiment_llm"}
    missing = required.difference(df.columns)

    if missing:
        raise ValueError(f"Faltan columnas: {', '.join(sorted(missing))}")
    if len(df) != 2000:
        raise ValueError(f"Se esperaban 2000 filas y se encontraron {len(df)}")

    mandatory = df[["id", "identifier", "text", "categoria"]]
    if mandatory.apply(lambda column: column.str.strip().eq("")).any().any():
        raise ValueError("Hay valores vacíos en las columnas obligatorias")
    if df["id"].duplicated().any() or df["identifier"].duplicated().any():
        raise ValueError("Hay identificadores duplicados")
    if not set(df["sentiment_llm"]).issubset(SENTIMENTS):
        raise ValueError("Hay etiquetas de sentimiento inválidas")
    return df


def make_category_quotas(df: pd.DataFrame) -> dict[str, int]:
    counts = df["categoria"].value_counts().to_dict()
    if len(counts) != 23:
        raise ValueError(f"Se esperaban 23 categorías y se encontraron {len(counts)}")

    # Ocho categorías reciben una fila extra para completar 100.
    quotas = {category: 4 for category in counts}
    by_size = sorted(counts, key=lambda category: (-counts[category], category))
    for category in by_size[:8]:
        quotas[category] = 5
    return quotas


def make_sentiment_quotas(
    df: pd.DataFrame,
    category_quotas: dict[str, int],
    generator: random.Random,
) -> dict[str, dict[str, int]]:
    allocation: dict[str, dict[str, int]] = {}
    selected = {label: 0 for label in SENTIMENTS}

    categories = sorted(category_quotas)
    for category in categories:
        rows = df[df["categoria"] == category]
        available = [label for label in SENTIMENTS if label in set(rows["sentiment_llm"])]
        current = {label: 1 for label in available}

        for _ in range(category_quotas[category] - sum(current.values())):
            candidates = available.copy()
            generator.shuffle(candidates)
            label = max(candidates, key=lambda item: SENTIMENT_TARGETS[item] - selected[item])
            current[label] += 1

        allocation[category] = current
        for label, amount in current.items():
            selected[label] += amount

    if selected != SENTIMENT_TARGETS:
        raise RuntimeError(f"No se pudo equilibrar el sentimiento: {selected}")
    return allocation


def select_sample(df: pd.DataFrame, seed: int) -> pd.DataFrame:
    generator = random.Random(seed)
    category_quotas = make_category_quotas(df)
    sentiment_quotas = make_sentiment_quotas(df, category_quotas, generator)
    selected_indices: list[int] = []

    # La etiqueta del LLM solo equilibra la selección.
    for category, quotas in sentiment_quotas.items():
        for sentiment, amount in quotas.items():
            matches = (df["categoria"] == category) & (df["sentiment_llm"] == sentiment)
            candidates = df.index[matches].tolist()
            selected_indices.extend(generator.sample(candidates, amount))

    generator.shuffle(selected_indices)
    sample = df.loc[selected_indices].reset_index(drop=True)
    if len(sample) != 100 or sample["id"].duplicated().any():
        raise RuntimeError("La muestra generada no es válida")
    return sample


def save_copies(sample: pd.DataFrame, overwrite: bool) -> tuple[Path, Path]:
    # Las predicciones no se muestran a los anotadores.
    output = sample[["id", "identifier", "text"]].copy()
    output["sentimiento_humano"] = ""
    output["ironia_humana"] = ""
    output = output[OUTPUT_COLUMNS]
    paths = (BASE_DIR / "anotador_1.csv", BASE_DIR / "anotador_2.csv")

    if not overwrite and any(path.exists() for path in paths):
        raise FileExistsError("Los archivos ya existen. Usa --overwrite para reemplazarlos.")
    for path in paths:
        output.to_csv(path, index=False, encoding="utf-8-sig", lineterminator="\n")
    return paths


def prepare_sample(seed: int, overwrite: bool) -> None:
    corpus = load_corpus(CORPUS_PATH)
    sample = select_sample(corpus, seed)
    paths = save_copies(sample, overwrite)

    print(f"Muestra creada con semilla {seed}")
    print("Categorías: 8 con 5 publicaciones y 15 con 4")
    print("Sentimiento provisional:", sample["sentiment_llm"].value_counts().to_dict())
    for path in paths:
        print(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepara la muestra para anotación humana.")
    parser.add_argument("--seed", type=int, default=20260905)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    prepare_sample(args.seed, args.overwrite)


if __name__ == "__main__":
    main()
