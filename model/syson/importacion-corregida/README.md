# Importación corregida de OpenSort V1

Evaluación local del 2026-11-15 con SysON `v2026.11.0`. El archivo de referencia
sigue siendo [`../../opensort.sysml`](../../opensort.sysml). Estos archivos son una
instantánea de verificación; no se editan como una segunda fuente principal.

## Correcciones

1. `entry` es palabra reservada. El puerto se declara como `port 'entry'` y la
   conexión usa `controller.'entry'`. Conserva el nombre del elemento y las seis
   interfaces; evita que el parser interrumpa la lectura antes de sus conexiones.
2. El exportador probado transforma `not (entrySensorClear and exitSensorsClear)`
   en `not entrySensorClear and exitSensorsClear`, perdiendo la agrupación. La
   referencia usa ahora la forma equivalente `not entrySensorClear or not
   exitSensorsClear`, que conserva su significado al exportar y reimportar.

Las vistas HTML siguen describiendo correctamente las interfaces y condiciones:
el nombre lógico del puerto no cambia y el rechazo sigue significando «algún
sensor ocupado». La simulación Python no cambió.

## Evidencia

- [opensort-export.sysml](opensort-export.sysml): texto descargado del modelo corregido.
- [opensort-project.zip](opensort-project.zip): proyecto completo tras importar la referencia.
- [reimported-project.zip](reimported-project.zip): proyecto nuevo creado importando el texto exportado.
- [verification.json](verification.json): hashes, informes de importación, contratos extraídos del JSON nativo y tabla de verdad del rearme.

Ambas importaciones devolvieron `UploadDocumentSuccessPayload` con informe vacío.
En el contenido nativo se comprobaron las definiciones `BenchStation`,
`PackageCycle` y `StationStates`, seis conexiones y seis transiciones de estado
(incluida la entrada inicial), con los mismos orígenes, destinos, eventos,
condiciones y efectos antes y después del intercambio.

Las condiciones extraídas de los árboles de expresiones de ambos proyectos dan:

| Entrada libre | Salidas libres | Aceptar rearme | Rechazar rearme |
|---|---|---|---|
| No | No | No | Sí |
| No | Sí | No | Sí |
| Sí | No | No | Sí |
| Sí | Sí | Sí | No |

La exportación y la segunda exportación tienen los mismos tokens al excluir
comentarios de documentación y espacios. Se conservan las cuatro decisiones del
ciclo; el cambio de bytes entre exportaciones corresponde a la indentación de la
documentación que añade el exportador.

El ZIP se cargó también desde **Upload project**. La navegación automática de esa
prueba agotó su espera, pero el servidor creó el proyecto; al descargarlo por API,
su contrato de conexiones y estados coincide con el original. Esto se registra
separadamente de la reimportación textual, que terminó sin advertencias.

## Reproducir y continuar

1. Inicia el [entorno local](../../../infra/syson/README.md).
2. Crea un proyecto nuevo e importa `model/opensort.sysml`; revisa que el informe
   esté vacío y que las tres definiciones aparezcan en el Explorer.
3. Descarga el documento `.sysml` y vuelve a importarlo en otro proyecto. Compara
   conexiones, ciclo y estados, en especial las dos condiciones de rearme.
4. Para recuperar esta instantánea, carga `opensort-project.zip` desde la pantalla
   **Upload project** de la página inicial.

En esta máquina el proyecto corregido se llama **OpenSort V1 corregido**, con ID
`6a9874e5-c744-4cd0-a6ac-b578656e239a`. Los IDs locales no son portables; usa el ZIP
en otra instancia.

Esta evidencia comprueba el intercambio del modelo lógico con esta versión de
SysON. No acredita ejecución del ciclo en un motor SysML ni validación física.
Los proyectos exportados no contienen representaciones gráficas: crear las vistas
de estructura, acciones y estados es el siguiente paso.
