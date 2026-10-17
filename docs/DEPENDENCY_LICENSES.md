# Inventario de licencias de dependencias

Fecha de revisión: 17 de octubre de 2026.

Se revisaron las entradas de `requirements.txt` contra las distribuciones instaladas, sin importar ni ejecutar las bibliotecas. Todas las versiones instaladas coinciden con las declaradas. Los datos se tomaron de `License-Expression`, `License`, clasificadores o, donde faltaban datos útiles, del archivo de licencia incluido.

Esta tabla conserva las declaraciones de los paquetes; valores genéricos como `BSD` o `Dual License` no se han convertido en identificadores SPDX por suposición. Los metadatos no sustituyen la lectura de los textos completos ni incluyen necesariamente todas las licencias del código nativo empaquetado. No es un inventario de todas las dependencias transitivas instaladas ni de una imagen Docker final.

Para la interpretación y los puntos pendientes, consultar [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). En particular, `pysentimiento` declara condiciones no comerciales y `ezsheets` GPLv3 o posterior.

Entradas revisadas: **101**.

| Paquete | Versión declarada e instalada | Licencia o declaración encontrada | Fuente en el paquete |
| --- | --- | --- | --- |
| `accelerate` | `1.14.0` | Apache | License |
| `aiohappyeyeballs` | `2.6.2` | PSF-2.0 | License |
| `aiohttp` | `3.14.1` | Apache-2.0 AND MIT | License |
| `aiosignal` | `1.4.0` | Apache 2.0 | License |
| `alembic` | `1.14.0` | MIT | License |
| `annotated-doc` | `0.0.4` | MIT | License-Expression |
| `annotated-types` | `0.7.0` | OSI Approved :: MIT License | Classifier |
| `anyio` | `4.13.0` | MIT | License-Expression |
| `attrs` | `26.1.0` | MIT | License-Expression |
| `beautifulsoup4` | `4.15.0` | MIT License | License |
| `blis` | `1.3.3` | BSD | License |
| `catalogue` | `2.0.10` | MIT | License |
| `certifi` | `2026.5.20` | MPL-2.0 | License |
| `charset-normalizer` | `3.4.7` | MIT | License |
| `click` | `8.4.1` | BSD-3-Clause | License-Expression |
| `cloudpathlib` | `0.24.0` | OSI Approved :: MIT License | Classifier |
| `confection` | `1.3.3` | MIT | License |
| `cymem` | `2.0.13` | MIT | License |
| `datasets` | `5.0.0` | Apache 2.0 | License |
| `dill` | `0.4.1` | BSD-3-Clause | License |
| `dotenv` | `0.9.9` | MIT | Archivo de licencia |
| `emoji` | `2.15.0` | OSI Approved :: BSD License | Classifier |
| `ezsheets` | `2026.4.28` | GPLv3+ | License |
| `fastapi` | `0.136.3` | MIT | License-Expression |
| `filelock` | `3.29.3` | MIT | License-Expression |
| `filetype` | `1.2.0` | MIT | License |
| `frozenlist` | `1.8.0` | Apache-2.0 | License |
| `fsspec` | `2026.4.0` | BSD-3-Clause | License-Expression |
| `h11` | `0.16.0` | MIT | License |
| `hf-xet` | `1.5.1` | Apache-2.0 | License-Expression |
| `httpcore` | `1.0.9` | BSD-3-Clause | License-Expression |
| `httpx` | `0.28.1` | BSD-3-Clause | License |
| `huggingface_hub` | `1.19.0` | Apache-2.0 | License |
| `idna` | `3.18` | BSD-3-Clause | License-Expression |
| `Jinja2` | `3.1.6` | OSI Approved :: BSD License | Classifier |
| `Js2Py_3.13` | `0.74.1` | MIT | License |
| `lxml` | `6.1.1` | BSD-3-Clause | License |
| `m3u8` | `6.0.0` | MIT | License |
| `markdown-it-py` | `4.2.0` | OSI Approved :: MIT License | Classifier |
| `MarkupSafe` | `3.0.3` | BSD-3-Clause | License-Expression |
| `mdurl` | `0.1.2` | OSI Approved :: MIT License | Classifier |
| `mpmath` | `1.3.0` | BSD | License |
| `multidict` | `6.7.1` | Apache License 2.0 | License |
| `multiprocess` | `0.70.19` | BSD-3-Clause | License |
| `murmurhash` | `1.0.15` | MIT | License |
| `networkx` | `3.6.1` | BSD-3-Clause | License-Expression |
| `numpy` | `2.4.6` | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | License-Expression |
| `packaging` | `26.2` | Apache-2.0 OR BSD-2-Clause | License-Expression |
| `pandas` | `3.0.3` | BSD-3-Clause (texto completo en el paquete) | License |
| `preshed` | `3.0.13` | MIT | License |
| `propcache` | `0.5.2` | Apache-2.0 | License |
| `psutil` | `7.2.2` | BSD-3-Clause | License |
| `psycopg` | `3.3.4` | LGPL-3.0-only | License-Expression |
| `psycopg-binary` | `3.3.4` | LGPL-3.0-only | License-Expression |
| `pyarrow` | `24.0.0` | Apache-2.0 | License-Expression |
| `pydantic` | `2.13.4` | MIT | License-Expression |
| `pydantic_core` | `2.46.4` | MIT | License-Expression |
| `Pygments` | `2.20.0` | BSD-2-Clause | License-Expression |
| `pyjsparser` | `2.7.1` | MIT | License |
| `pyotp` | `2.9.0` | MIT License | License |
| `pysentimiento` | `0.7.3` | Condición propia: no comercial e investigación científica | Archivo de licencia |
| `python-dateutil` | `2.9.0.post0` | Dual License | License |
| `python-dotenv` | `1.2.2` | BSD-3-Clause | License |
| `PyYAML` | `6.0.3` | MIT | License |
| `regex` | `2026.5.9` | Apache-2.0 AND CNRI-Python | License-Expression |
| `requests` | `2.34.2` | Apache-2.0 | License |
| `rich` | `15.0.0` | MIT | License |
| `safetensors` | `0.8.0` | OSI Approved :: Apache Software License | Classifier |
| `setuptools` | `81.0.0` | MIT | License-Expression |
| `shellingham` | `1.5.4` | ISC License | License |
| `six` | `1.17.0` | MIT | License |
| `smart_open` | `7.6.1` | OSI Approved :: MIT License | Classifier |
| `socksio` | `1.0.0` | OSI Approved :: MIT License | Classifier |
| `soupsieve` | `2.8.4` | MIT | License-Expression |
| `spacy` | `3.8.13` | MIT | License |
| `spacy-legacy` | `3.0.12` | MIT | License |
| `spacy-loggers` | `1.0.5` | MIT | License |
| `SQLAlchemy` | `2.0.50` | MIT | License |
| `sqlmodel` | `0.0.38` | MIT | License-Expression |
| `srsly` | `2.5.3` | MIT | License |
| `starlette` | `1.2.1` | BSD-3-Clause | License-Expression |
| `sympy` | `1.14.0` | BSD | License |
| `thinc` | `8.3.13` | MIT | License |
| `tokenizers` | `0.22.2` | OSI Approved :: Apache Software License | Classifier |
| `torch` | `2.12.0` | BSD-3-Clause | License |
| `tqdm` | `4.68.2` | MPL-2.0 AND MIT | License |
| `transformers` | `5.12.0` | Apache 2.0 License | License |
| `twikit` | `2.3.3` | MIT | License |
| `typer` | `0.25.1` | MIT | License-Expression |
| `typing-inspection` | `0.4.2` | MIT | License-Expression |
| `typing_extensions` | `4.15.0` | PSF-2.0 | License-Expression |
| `tzlocal` | `5.3.1` | MIT | License |
| `urllib3` | `2.7.0` | MIT | License-Expression |
| `uvicorn` | `0.49.0` | BSD-3-Clause | License-Expression |
| `wasabi` | `1.1.3` | MIT | License |
| `weasel` | `1.0.0` | MIT | License |
| `webvtt-py` | `0.5.1` | MIT | License |
| `wrapt` | `2.2.1` | BSD-2-Clause | License-Expression |
| `xdk` | `0.10.6` | OSI Approved :: MIT License | Classifier |
| `xxhash` | `3.7.0` | BSD | License |
| `yarl` | `1.24.2` | Apache-2.0 | License |
