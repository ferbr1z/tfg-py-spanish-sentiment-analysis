# Clasificador LLM

Clasificación de publicaciones de X en el contexto paraguayo: sentimiento, tipo de fuente, idioma, ironía y motivos de descarte.

[Prompt vigente](prompt.txt) · [Esquema de salida](output_schema.json) · [Workflow de n8n](../TFG%20Pipeline.json) · [Documentación general](../README.md)

## Archivos de referencia

| Archivo | Función |
| --- | --- |
| [prompt.txt](prompt.txt) | Prompt vigente, versión `5`, sincronizado con `LLM Sentiment Classifier` |
| [output_schema.json](output_schema.json) | Copia JSON del esquema de `Validate LLM Output` en el workflow |

`prompt.txt` es el único archivo de prompt de esta carpeta. La versión `5` alinea los identificadores y las reglas de descarte con el flujo de carga. Las versiones anteriores pueden consultarse en el historial de Git.

## Flujo de clasificación

1. `Scrapper` entrega las publicaciones en `items`, con `id` y `text` como campos necesarios para clasificar.
2. `LLM Sentiment Classifier` aplica el prompt usando el modelo de `OpenAI Chat Model`.
3. `Validate LLM Output` interpreta la respuesta estructurada con el esquema del workflow.
4. `Code in JavaScript` comprueba identificadores y reglas de descarte, recupera los datos originales y agrega los metadatos del LLM.
5. `Upload` envía el lote a `/upload-data/{subtopic_id}` para su almacenamiento mediante la API.

Las publicaciones evidentemente ajenas a Paraguay se omiten. Las incluidas se clasifican por fuente y sentimiento; las predominantemente en guaraní o ininteligibles se conservan con `discarded=true` y el motivo correspondiente.

## Contrato de salida del LLM

La respuesta es un **arreglo JSON**, no un objeto con `classifications`. Puede contener menos elementos que la entrada debido a las omisiones geográficas. Si no hay publicaciones incluidas, devuelve `[]`.

```json
[
  {
    "id": "1234567890",
    "llm_reason": "Expresa una queja explícita sobre el servicio",
    "source_type": "ciudadano",
    "sentiment_llm": "NEG",
    "has_irony": false,
    "mixed": false,
    "lang": "es",
    "discarded": false,
    "discard_reason": null
  }
]
```

Todos los campos son obligatorios y el esquema no admite propiedades adicionales.

| Campo | Valores y significado |
| --- | --- |
| `id` | Identificador original como cadena, sin modificar, inventar ni duplicar |
| `llm_reason` | Justificación breve; el prompt pide un máximo de 12 palabras |
| `source_type` | `ciudadano`, `medio`, `institucional` u `otro` |
| `sentiment_llm` | `POS`, `NEG` o `NEU`, también cuando el registro está descartado |
| `has_irony` | Presencia de ironía o sarcasmo detectable en el texto |
| `mixed` | Sentimientos positivo y negativo genuinamente equilibrados; no mezcla de idiomas |
| `lang` | `es` o `jopara`; `null` para los descartados |
| `discarded` | Indica descarte por idioma o ininteligibilidad, no por procedencia geográfica |
| `discard_reason` | `guarani` o `ininteligible` cuando se descarta; `null` en otro caso |

### Esquema y reglas de aplicación

[output_schema.json](output_schema.json) reproduce el esquema del pipeline, sin endurecerlo ni cambiar sus nombres. Ese esquema permite `sentiment_llm=null`, pero el prompt vigente, el nodo de preparación y [PostCreateSchema](../schemas.py) exigen una etiqueta no nula. El esquema es más permisivo que el contrato efectivo de carga.

- `discarded=false`: `lang` es `es` o `jopara` y `discard_reason=null`.
- `discarded=true`: `lang=null`, el motivo es `guarani` o `ininteligible` y se conserva una etiqueta de sentimiento. Para texto ininteligible se usa `NEU`.
- Un ID desconocido o repetido hace fallar la preparación del lote.
- La omisión geográfica no genera un registro descartado: el ID queda fuera del arreglo y se informa en `omitted_other_country` durante la preparación.

El JSON Schema valida estructura y tipos. Las relaciones entre campos se verifican en el nodo de código; otros criterios, como la justificación de hasta 12 palabras, son instrucciones del prompt y no límites implementados en el esquema.

## Del resultado del LLM al registro de la API

El nodo `Code in JavaScript` transforma `id` en `identifier` y recupera los campos de la publicación original, como `text` y `created_at`. También agrega:

| Campo | Origen |
| --- | --- |
| `llm_model` | Variable de entorno `MODEL` de n8n |
| `llm_prompt_version` | Versión `5` declarada en el nodo |
| `llm_classified_at` | Fecha y hora de preparación del lote, en formato ISO |

El nodo produce un objeto que contiene `items` y el estado del subtema, no un elemento de n8n por publicación. `Upload` utiliza ese arreglo como cuerpo de la solicitud y transmite el token de paginación por query string.

## Configuración en n8n

1. Sigue la [instalación del proyecto y de n8n](../README.md#integraciones).
2. Importa [TFG Pipeline.json](../TFG%20Pipeline.json).
3. Configura una credencial del proveedor en `OpenAI Chat Model`.
4. Define `MODEL` y `API_URL` en `.env`; `SINCE_DATE` y `UNTIL_DATE` son opcionales. Compose transmite estos valores al contenedor; recréalo si cambias su entorno.
5. Prueba un lote pequeño antes de activar la programación del workflow.

El workflow exportado contiene su propia copia del prompt y del esquema: n8n **no lee automáticamente** los archivos de esta carpeta. Al importar el workflow actualizado, no hace falta copiarlos manualmente.

La API key se guarda en las credenciales de n8n, nunca en el prompt, el workflow exportado ni los archivos del repositorio.

## Cómo mantenerlo sincronizado

Al modificar los criterios o el contrato:

1. Edita [prompt.txt](prompt.txt) y copia su contenido al campo `text` de `LLM Sentiment Classifier`, conservando el modo expresión y la interpolación `{{ JSON.stringify($json.items) }}`.
2. Si cambia el esquema, actualiza tanto [output_schema.json](output_schema.json) como `Validate LLM Output`. El nodo actual genera el esquema mediante una expresión; ambos deben representar el mismo JSON.
3. Revisa `Code in JavaScript` y `PostCreateSchema` para mantener compatibles los nombres, valores nulos y reglas de descarte.
4. Incrementa `llm_prompt_version` en el nodo de preparación y documenta la versión aquí. No reetiquetes registros históricos como si hubieran usado el nuevo prompt.
5. Verifica un lote vacío, una publicación normal, una descartada y las omisiones geográficas. Comprueba también que se rechacen IDs ajenos o duplicados.

Los cambios de criterio pueden afectar la comparabilidad del corpus; conserva su trazabilidad mediante la versión y el historial de Git.
