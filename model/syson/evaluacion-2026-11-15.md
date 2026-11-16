# Primera importación en SysON v2026.11.0

## Entrada y procedimiento

Evaluación local del 2026-11-15, con el modelo de `main` en `cc2e849`, sin modificarlo:

- Archivo: `model/opensort.sysml`, 7291 bytes.
- SHA-256: `679108165bb39c3348c04e612a8e52f3e2987583d32c25f38f0994b180a76040`.
- SysON: `eclipsesyson/syson:v2026.11.0`; PostgreSQL: `postgres:15.20`.
- Proyecto nuevo de evaluación, importación mediante `uploadDocument` de GraphQL,
  descarga del ZIP del proyecto y del documento textual. Se utilizaron los endpoints
  documentados en el [recetario de la versión](https://doc.mbse-syson.org/syson/v2026.11.0/developer-guide/api/api-cookbook.html).

## Resultado observado

La respuesta fue `UploadDocumentSuccessPayload`, pero incluyó una advertencia de
error de sintaxis y posible pérdida de los elementos posteriores. El informe indica
la línea 73 del archivo original, que contiene `port entry : ~EntrySignal;`, y una
referencia no resuelta a `StationStates` en `controller::operatingStates`.

Esto identifica dónde informa el importador; no establece todavía si cada problema
proviene del archivo, de una limitación de SysON o de ambos. La corrección requiere
una revisión específica de la sintaxis y del resultado completo.

El texto exportado tiene 2365 bytes: conserva `BenchStation` y `resetButton`, pero
no incluye las definiciones `PackageCycle` ni `StationStates`. El ZIP descargado
tiene 11147 bytes y su manifiesto contiene un documento `opensort.sysml` y ninguna
representación gráfica.

Reimportar ese texto en otro proyecto terminó con informe vacío. **Ese resultado
solo corresponde al subconjunto exportado; no valida el modelo original completo.**
El ZIP se pudo cargar desde la pantalla Upload project y abrió la ruta de un nuevo
editor. No se acredita todavía equivalencia gráfica ni conservación de diagramas,
puesto que el proyecto evaluado no tenía representaciones.

## Decisión de continuidad

No se sustituye la referencia por la exportación parcial ni se versiona esta como
un modelo aceptado. Los artefactos parciales y el informe completo permanecen en
la máquina de evaluación, bajo `/tmp/opensort-syson-evaluation/`, y los proyectos
locales se conservan en el volumen. Esos archivos temporales no son un respaldo
duradero; este registro conserva la evidencia necesaria para repetir el caso.

La siguiente tarea de modelado es resolver el informe, recuperar las seis
interfaces, el flujo y los estados, y volver a comprobar exportación/reimportación
de texto y proyecto completo antes de adoptar SysON como editor principal.
