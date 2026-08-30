# Clasificador LLM

Esta parte del pipeline clasifica publicaciones paraguayas como `POS`, `NEG` o `NEU` y detecta ironía o sarcasmo mediante el modelo configurado en `MODEL`.

## Contrato de entrada

El nodo `Scrapper` debe entregar un objeto `items`. Cada publicación necesita como mínimo `id` y `text`.

## Contrato de salida

El LLM devuelve `output.classifications`, una lista con un objeto por publicación:

```json
{
  "classifications": [
    {
      "id": "publicacionid",
      "label": "NEG",
      "hasIrony": true
    }
  ]
}
```

`Prepare LLM Results` produce un elemento de n8n por publicación. Conserva todos los campos originales y agrega:

- `sentiment_llm`: `POS`, `NEG` o `NEU`.
- `hasIrony`: `true` cuando se detecta ironía o sarcasmo; de lo contrario, `false`.
- `llm_model`: identificador del modelo utilizado.
- `llm_prompt_version`: versión del prompt.
- `llm_classified_at`: fecha y hora ISO de clasificación.

Esos elementos pueden conectarse directamente a los nodos encargados de Google Sheets y de la base de datos externa.

## Única configuración manual del LLM

1. Importar `n8n.json` en n8n.
2. Abrir `OpenAI Chat Model`.
3. Crear una credencial de OpenAI, pegar la API key y guardar.

El modelo, el prompt, los criterios de clasificación, la validación y la
preparación de resultados ya quedan configurados en el workflow. No hay que
copiar el prompt ni editar el esquema manualmente.

Al ejecutar, `Prepare LLM Results` entrega una fila por publicación lista para
conectarse a Google Sheets o a la base de datos externa.

El prompt actual está en `prompt_v4.txt` y su esquema de validación en `output_schema.json`.

La API key se guarda únicamente en la credencial de n8n. No debe agregarse a
`n8n.json`, `.env`, el prompt ni ningún archivo del repositorio.

## Dónde está cada parte

- `../TFG Pipeline.json`: workflow que conecta scraper, clasificador, validación y
  preparación de resultados.
- `prompt_v4.txt`: copia versionada del criterio de clasificación usado en el
  nodo `LLM Sentiment Classifier`.
- `output_schema.json`: contrato de salida usado por `Validate LLM Output`.
- Credencial de OpenAI: solamente en el nodo `OpenAI Chat Model` de n8n.

Si se cambia el prompt o el esquema, se debe actualizar tanto el archivo
versionado como el nodo correspondiente de `TFG Pipeline.json`.
