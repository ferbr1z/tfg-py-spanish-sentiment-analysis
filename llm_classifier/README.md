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
- `real_validation_sample.json`: publicaciones reales obtenidas por el scraper
  y la clasificación devuelta por el workflow LLM.
- Credencial de OpenAI: solamente en el nodo `OpenAI Chat Model` de n8n.

Si se cambia el prompt o el esquema, se debe actualizar tanto el archivo
versionado como el nodo correspondiente de `n8n.json`.

## Prueba verificada con publicaciones reales

El 23 de agosto de 2026 se recolectaron cinco publicaciones reales de
X/Twitter mediante el scraper del proyecto con la consulta `Paraguay lang:es`.
La muestra se envió al clasificador real de n8n usando `gpt-5-mini`, la
credencial configurada y el esquema estructurado.

En los cinco casos se conservó el identificador original y la respuesta quedó
dentro del conjunto permitido `POS`, `NEG` o `NEU`. La consulta, la fecha de
recolección, los textos y las respuestas se conservan en
`real_validation_sample.json`.

Esta evidencia demuestra que la integración scraper–LLM funciona con datos
reales. No mide por sí sola la exactitud de las clasificaciones; para afirmar
exactitud sería necesaria una muestra real etiquetada manualmente.
