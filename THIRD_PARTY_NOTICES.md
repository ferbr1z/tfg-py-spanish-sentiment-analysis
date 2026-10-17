# Componentes y avisos de terceros

Revisión realizada el 17 de octubre de 2026 sobre las versiones fijadas en `requirements.txt` y sus distribuciones instaladas. La licencia MIT de este repositorio corresponde a los aportes propios de sus autores; no sustituye los derechos ni las condiciones de terceros.

## Resultado de la revisión

La configuración actual **no debe presentarse como una aplicación completa habilitada para cualquier uso bajo MIT**. Se identificaron condiciones adicionales en `pysentimiento`, los modelos descargados, `ezsheets` y el servicio externo n8n. Añadir créditos no elimina esas condiciones.

| Componente | Evidencia revisada | Resultado |
| --- | --- | --- |
| `twikit==2.3.3` | Licencia del paquete instalado y repositorio de origen | MIT; conservar copyright y permiso en código incorporado o adaptado |
| `xdk==0.10.6` | Metadatos del paquete instalado | Declara MIT; el paquete instalado no incluye un archivo de licencia separado. Verificar el texto correspondiente al artefacto antes de redistribuirlo |
| `pandas==3.0.3` | Licencia incluida en la distribución | BSD-3-Clause; conservar los avisos exigidos si se redistribuye |
| `pysentimiento==0.7.3` | `LICENSE.md` incluido en la distribución instalada | Declara uso no comercial e investigación científica; no se comprobó una autorización comercial alternativa |
| `ezsheets==2026.4.28` | Metadatos y `LICENSE.txt` incluidos en la distribución | GPLv3 o posterior; la integración debe evaluarse antes de distribuir una aplicación combinada bajo condiciones exclusivamente MIT |
| `psycopg==3.3.4` y `psycopg-binary==3.3.4` | Metadatos y licencias de las distribuciones instaladas | LGPL-3.0-only; revisar sus obligaciones al redistribuir, incluidas las de las bibliotecas nativas empaquetadas |
| `certifi==2026.5.20` | Metadatos del paquete instalado | MPL-2.0; conservar las condiciones aplicables a sus archivos al redistribuir |
| n8n | Licencia publicada por el proyecto de origen | Sustainable Use License para las partes cubiertas por ella y condiciones separadas para otras partes; no queda cubierto por nuestra MIT |

El [inventario de dependencias](docs/DEPENDENCY_LICENSES.md) registra todas las entradas de `requirements.txt`, sus versiones y las declaraciones encontradas. No se detectaron diferencias de versión entre esas entradas y el entorno revisado.

## Código adaptado de Twikit y twifork

Se identificaron estas referencias explícitas de procedencia en el código:

- [`scrapper/old/compat/twikit_patches.py`](scrapper/old/compat/twikit_patches.py): adaptación de la búsqueda y del procesamiento de respuestas, con referencia al [PR #419 de d60/twikit](https://github.com/d60/twikit/pull/419), presentado por `sakenuGOD`.
- [`scrapper/old/compat/transaction.py`](scrapper/old/compat/transaction.py): compatibilidad con el cálculo de transacciones de Twikit y corrección de redondeo atribuida en el archivo al fork [PawiX25/twifork](https://github.com/PawiX25/twifork).

Los archivos locales contienen modificaciones de este proyecto. Se conserva el aviso original `Copyright (c) 2024 d60` y el texto MIT en [`licenses/twikit-MIT.txt`](licenses/twikit-MIT.txt). La [licencia publicada por twifork](https://github.com/PawiX25/twifork/blob/main/LICENSE) conserva ese mismo aviso.

Las referencias anteriores proceden de los comentarios locales y de las fuentes consultadas. No se ha determinado el commit exacto de origen de cada fragmento; esa trazabilidad queda pendiente y no se atribuye la autoría exclusiva de esos fragmentos a los autores de este repositorio.

## pysentimiento y modelos

La distribución instalada de `pysentimiento==0.7.3` incluye una declaración de uso no comercial e investigación científica. Se conserva su texto exacto en [`licenses/pysentimiento-0.7.3.txt`](licenses/pysentimiento-0.7.3.txt). Una declaración diferente en una versión posterior no modifica automáticamente las condiciones de la versión instalada.

La configuración predeterminada de esa versión selecciona estos modelos para las llamadas de `sentiment_analyzer/analyzer.py`:

| Tarea | Modelo | Documentación |
| --- | --- | --- |
| Sentimiento en español | `pysentimiento/robertuito-sentiment-analysis` | [Ficha del modelo](https://huggingface.co/pysentimiento/robertuito-sentiment-analysis) |
| Emociones en español | `pysentimiento/robertuito-emotion-analysis` | [Ficha del modelo](https://huggingface.co/pysentimiento/robertuito-emotion-analysis) |

Las fichas relacionan los modelos con TASS 2020 y solicitan citas de los trabajos utilizados. El [proyecto pysentimiento](https://github.com/pysentimiento/pysentimiento#license) advierte que los modelos dependen de licencias de datasets de terceros, muchas de ellas para uso no comercial. La documentación consultada no establece un permiso comercial general para estos dos modelos.

Para trabajos académicos, revisar las citas solicitadas en las fichas de cada modelo: pysentimiento, RoBERTuito, TASS y, en la ficha de emociones, EmoEvent. Las citas académicas y los permisos de uso son cuestiones distintas: citar no concede derechos adicionales.

No se fijan revisiones de los modelos en el código actual. Esta revisión identifica los modelos predeterminados de la biblioteca, pero no certifica el contenido ni la revisión exacta de la caché local, ni reproduce todos los términos de los datasets originales.

## Google Sheets y GPL

`handlers/google_sheets.py` importa `ezsheets` y utiliza sus clases en el mismo proceso. Que la integración sea opcional no demuestra por sí solo que una distribución combinada pueda ofrecerse exclusivamente bajo MIT.

La GPL permite uso comercial, pero establece condiciones de distribución y disponibilidad del código fuente. Antes de distribuir una aplicación que incorpore esta integración, debe resolverse cómo cumplir las condiciones de la combinación. Para mantener el objetivo de una distribución permisiva, una alternativa técnica es sustituir `ezsheets` por un cliente con licencia compatible con ese objetivo. Esta revisión no cambia dependencias ni relicencia el código.

Fuente: `License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)` y `LICENSE.txt` del paquete instalado; [proyecto de origen](https://github.com/asweigart/ezsheets) y [texto de GPLv3](https://www.gnu.org/licenses/gpl-3.0.html).

## Servicios, imágenes y publicaciones de X

- [`docker-compose.yml`](docker-compose.yml) referencia `n8nio/n8n:latest`; no fija una versión concreta. Consultar la licencia de la imagen efectivamente utilizada antes de redistribuirla u ofrecer un servicio basado en ella. La [licencia publicada de n8n](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) incluye limitaciones de uso y distribución.
- El acceso a X y al proveedor del LLM se rige también por sus términos de servicio. La licencia de un cliente Python no concede derechos sobre esos servicios.
- Las publicaciones recolectadas no pasan a estar bajo MIT por almacenarse con esta aplicación. Antes de publicar un corpus, evaluar los derechos sobre los textos y las condiciones de la fuente.

## Alcance y pendientes

Esta es una revisión documental y técnica de las dependencias declaradas y de las referencias explícitas de código adaptado. No es una certificación de cumplimiento de una distribución final.

Antes de anunciar una aplicación completa para cualquier uso, quedan por resolver:

1. Obtener permisos adecuados para `pysentimiento==0.7.3` y los modelos utilizados, o sustituir los componentes cuyas condiciones no permitan el uso previsto.
2. Resolver la distribución de la integración GPL de Google Sheets.
3. Fijar la versión de n8n y las revisiones de los modelos para hacer reproducible su revisión.
4. Al preparar un ejecutable, imagen o paquete con dependencias incluidas, inventariar también las dependencias transitivas y bibliotecas nativas realmente distribuidas, conservar sus licencias y avisos y cumplir las obligaciones de código fuente que correspondan.

No es necesario incluir todas las bibliotecas en la portada del README. Este documento y el inventario permiten mantener esa presentación breve sin ocultar las condiciones identificadas.
