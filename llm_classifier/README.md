# Clasificador LLM

Esta parte del pipeline clasifica publicaciones paraguayas como `POS`, `NEG` o `NEU` mediante `gpt-5-mini`.

## Contrato de entrada

El nodo `Scrapper` debe entregar un objeto `items`. Cada publicación necesita como mínimo `id` y `text`.

## Contrato de salida

`Prepare LLM Results` produce un elemento de n8n por publicación. Conserva todos los campos originales y agrega:

- `sentiment_llm`: `POS`, `NEG` o `NEU`.
- `llm_model`: identificador del modelo utilizado.
- `llm_prompt_version`: versión del prompt.
- `llm_classified_at`: fecha y hora ISO de clasificación.

Esos elementos pueden conectarse directamente a los nodos encargados de Google Sheets y de la base de datos externa.

## Configuración

1. Importar `n8n.json` en n8n.
2. Abrir `OpenAI Chat Model` y seleccionar una credencial de OpenAI.
3. Ejecutar primero con un lote pequeño de publicaciones.
4. Comprobar que `Prepare LLM Results` produce una fila por publicación.

El prompt versionado está en `prompt_v1.txt` y su esquema de validación en `output_schema.json`.

La API key se guarda únicamente en la credencial de n8n. No debe agregarse a
`n8n.json`, `.env`, el prompt ni ningún archivo del repositorio.

## Dónde está cada parte

- `../n8n.json`: workflow que conecta scraper, clasificador, validación y
  preparación de resultados.
- `prompt_v1.txt`: copia versionada del criterio de clasificación usado en el
  nodo `LLM Sentiment Classifier`.
- `output_schema.json`: contrato de salida usado por `Validate LLM Output`.
- Credencial de OpenAI: solamente en el nodo `OpenAI Chat Model` de n8n.

Si se cambia el prompt o el esquema, se debe actualizar tanto el archivo
versionado como el nodo correspondiente de `n8n.json`.
