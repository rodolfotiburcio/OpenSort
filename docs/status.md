# OpenSort — Estado del proyecto

Última actualización: 2026-11-15.

## Hito actual

V0 — Simulador de una estación logística implementado y validado localmente.
V1 — Modelo lógico de la estación de banco y visualización HTML integrados en `main` mediante el PR #2 (commit `2915aa4`). Los estados y el rearme están integrados mediante el PR #3 (`6ce304b`); la pizarra HTML navegable y la corrección del relleno de las flechas, mediante el PR #4 (`b952453`). El motor persistente, el rearme y la simulación 2D se integraron en `main` mediante el PR #5 (`4c45618`). La implementación física sigue pendiente.

La entrega SysON reúne el entorno local v2026.11.0 con Compose y PostgreSQL 15.20,
la corrección de importación del modelo y tres vistas gráficas nativas. Se desarrolló
en las ramas dependientes `feature/syson-local`, `fix/syson-import` y
`feature/syson-views`, desde `cc2e849`. Consulta la
[entrega de vistas](../model/syson/vistas-v1/README.md) para abrirlas y recuperarlas.

**Hito de comprobación con una herramienta SysML: completado para el modelo lógico
de V1 en SysON v2026.11.0.** Se verificaron importación sin advertencias, conservación
de contratos al exportar/reimportar y recuperación de diagramas. Esto acredita la
compatibilidad comprobada con esa versión; la ejecución del comportamiento en un
motor SysML y la validación física siguen pendientes. `model/opensort.sysml` conserva
su condición de referencia textual; adoptar SysON como editor principal requiere
una decisión explícita sobre el flujo de edición.

## Último resultado verificado

El lote de demostración de V0 confirma salidas, envía paquetes a revisión y bloquea la admisión ante una discrepancia. Las pruebas automatizadas cubren confirmación, causas de revisión, timeout, salida incorrecta y reprocesamiento. Consulta los [comandos de reproducción](../README.md#ejecutar).

En la revisión de cierre del 2026-11-15 pasaron las once pruebas con `python3 -m unittest discover -s tests -v` y `git diff --check main...HEAD` no detectó errores de espacios. También se verificó la demo `python3 -m opensort --scenario wrong-exit`. En la simulación integrada, el bloqueo persiste entre llamadas y requiere rearme para volver a admitir paquetes; la sesión se conserva en memoria mientras el servidor está activo, sin persistencia en disco.

El usuario confirmó que el [modelo SysML](../model/opensort.sysml) es correcto. El modelo documenta seis interfaces: detección de entrada, resultado QR, consulta y respuesta del manifiesto, orden de desvío, confirmación de salida y solicitud de rearme. La [vista HTML](estacion-v1.html) representa el ciclo, las interfaces y los estados de la estación; su actualización es manual.

La [pizarra navegable](pizarra-v1.html) reúne componentes, ciclo, estados y diccionario de datos y puertos. Se revisó localmente en Chrome y el usuario confirmó su funcionamiento general. Se corrigió y verificó visualmente el relleno accidental de las flechas de `StationStates`. Ambas vistas HTML son manuales; esta revisión no valida la sintaxis SysML con una herramienta compatible.

## Decisiones confirmadas

- Un paquete por ciclo, tres salidas de destino y una salida de revisión.
- Sin QR, QR ilegible (incluido timeout de lectura), ID desconocido o destino sin ruta: enviar a revisión.
- Manifiesto no encontrado o no disponible: enviar a revisión, igual que ante un QR ausente o ilegible. Esta política ya está reflejada en SysML y HTML.
- Toda salida, incluida revisión, requiere confirmación física.
- Una salida incorrecta o un timeout de confirmación bloquea la admisión del siguiente paquete.

- Rearme mediante botón físico: el operador confirma que inspeccionó y despejó la estación.
- El ESP32 acepta la nueva pulsación solo estando bloqueado y con entrada y todas las salidas libres; registra el rearme, conserva el resultado fallido y habilita la admisión sin iniciar movimiento.
- Si hay sensores ocupados, registra el rechazo y mantiene el bloqueo. Se requiere otra pulsación; el botón mantenido o una solicitud anterior no producen rearme automático.
- Los sensores libres no certifican que el espacio entre ellos esté vacío: se requiere inspección del operador.

## Siguiente tarea

Concretar el contrato de hardware de V1: componentes, pines, polaridades, filtrado,
protocolos, tiempos, actuador y acceso al manifiesto, antes de implementar firmware.
Las vistas de estructura, ciclo y estados ya están creadas sobre los elementos
existentes y se conservan mediante el ZIP completo del proyecto.
La [evaluación corregida](../model/syson/importacion-corregida/README.md) documenta
la importación completa y el intercambio; la
[evaluación inicial](../model/syson/evaluacion-2026-11-15.md) se conserva como
histórico del fallo.

La simulación ya está integrada en `main` mediante
el PR #5. Para reproducirla: `uv run opensort --web` (o `--port 8001`).

La simulación incorpora estados persistentes, cola, animación, sensores sintéticos, pausa y velocidad, fallos de salida y rearme mediante nueva pulsación. Once pruebas automatizadas cubren las reglas y la API local. La revisión automatizada en Chrome verificó las rutas A/B/C, revisión, timeout, rechazo y aceptación del rearme y pausa posterior, sin errores JavaScript ni desbordamiento horizontal en móvil. La simulación usa biblioteca estándar de Python y recursos web incluidos en el paquete, sin dependencias de ejecución adicionales.

Criterio de revisión: provocar un fallo, comprobar que la cola no se admite, rechazar rearme antes de inspeccionar o con sensores ocupados, aceptar otra pulsación tras despejar y reanudar explícitamente la alimentación. El historial debe conservar el fallo. La importación y reimportación del modelo ya se comprobaron en SysON v2026.11.0; su ejecución en un motor SysML y la validación física siguen pendientes.

## Pendientes posteriores

- Concretar pines, polaridades, filtrado, protocolos, formatos, tiempos y actuador.
- Definir la ubicación y el acceso al manifiesto.
- Integrar lector QR, ESP32, sensores y desviador; comprobar la política de manifiesto no disponible en la implementación.
- Ampliar las vistas de SysON cuando se detalle V1 y guardar cada entrega como proyecto completo.
- Definir la secuencia de arranque y conectar las lecturas actuales de sensores y los eventos del ciclo a la máquina de estados.
- Tras validar el simulador, implementar y probar el rearme en firmware con sensores y botón físicos.
- Publicar la visualización mediante GitHub Pages y evaluar su generación automática desde el modelo.

## Desarrollo con IA

El 2026-11-15 se incorporaron `AGENTS.md`, tres skills de proyecto para simulador,
web y modelo, dos perfiles de agente para revisión y análisis de contratos,
configuración MCP opcional y plantilla de PR. La [guía de desarrollo con IA](ai-development.md)
incluye ejemplos de pedidos, delegación y continuidad; la [guía MCP](mcp.md)
documenta activación y autenticación. Esta incorporación aporta instrucciones y
configuración para el desarrollo.

Esa entrega se integró mediante el PR #6 (`cc2e849`). Las instrucciones y la guía
incorporan la creación de una rama por tarea antes de editar y la comprobación del
diff contra la base del PR.

Verificación de esta entrega: `uv run pytest -v` terminó con 11 pruebas y 20
subpruebas aprobadas. Se ejecutaron `uv run opensort` y
`uv run opensort --scenario wrong-exit`, con bloqueo final por `exit_timeout` y
`wrong_exit`, respectivamente. Las tres skills pasaron `quick_validate.py` de
`skill-creator`; se comprobaron los TOML y los enlaces locales de los archivos
añadidos. `codex mcp get` reconoció ambos servidores como desactivados. La revisión
final de espacios con `git diff --check` y de los archivos nuevos no detectó errores.

La autenticación y las consultas MCP remotas, así como la ejecución de los perfiles
de agente, quedan pendientes de una sesión que los necesite. Los ejemplos no
contienen credenciales ni modifican la configuración global. El siguiente paso
funcional sigue siendo el indicado arriba; para retomar, inicia Codex desde la raíz
y proporciona un objetivo y criterio de aceptación según la guía.

## Entorno SysON

La [guía local](../infra/syson/README.md) documenta arranque, persistencia, respaldo,
restauración y exportaciones. El [ADR 002](adr/0002-syson-local.md) acepta el entorno
local y mantiene pendiente su adopción como editor principal. Se añadieron tareas
de VS Code y el skill `opensort-syson`; se reutilizan los perfiles existentes.

Verificación inicial del entorno realizada el 2026-11-15:

- `docker compose -f infra/syson/compose.yaml config --quiet`: configuración válida.
- `up -d --wait --wait-timeout 180`: SysON y PostgreSQL en estado `healthy`;
  `/actuator/health` devuelve `UP`. Elasticsearch es opcional y no está desplegado;
  solo su comprobación de salud está desactivada.
- Inicio en Chrome mediante Playwright temporal, creación de proyectos e
  importación por API. Exportación textual y ZIP; reimportación del texto parcial
  sin informe y carga del ZIP desde el navegador. Esto no valida el modelo completo.
- `down` seguido de `up`: se conservaron los tres proyectos con los mismos IDs.
- `pg_dump -Fc` y `pg_restore --no-owner --exit-on-error` en el proyecto separado
  `opensort-syson-restore`: recuperados los dos proyectos presentes al respaldar;
  el JSON del proyecto evaluado coincide con el del ZIP anterior al respaldo.
  La instancia de restauración quedó detenida conservando su volumen.
- `uv run pytest -v`: 11 pruebas y 20 subpruebas aprobadas. Los skills nuevo y de
  modelo pasaron `quick_validate.py`; se comprobaron enlaces locales, tareas,
  exclusión de `.env`/respaldos y espacios con `git diff --check`.

En esa entrega no se cambió el modelo ni las vistas HTML. Los cambios del navegador
no se sincronizan con Git.

## Reparación de la importación

El 2026-11-15, en `fix/syson-import`, se corrigió el uso de la palabra reservada
`entry`: el puerto y su referencia se escriben como `'entry'`, sin cambiar su
nombre lógico. También se reescribió el rechazo del rearme con la condición
equivalente `not entrySensorClear or not exitSensorsClear`, porque el exportador
probado elimina la agrupación de `not (entrySensorClear and exitSensorsClear)`.

Comprobaciones realizadas sobre proyectos nuevos, sin sustituir los anteriores:

- Importación de `model/opensort.sysml` y reimportación de su exportación textual:
  `UploadDocumentSuccessPayload` con informe vacío en ambos casos.
- Presencia de `BenchStation`, `PackageCycle` y `StationStates`, seis conexiones,
  seis transiciones (incluida la inicial) y cuatro decisiones del ciclo.
- Contratos de conexiones y estados iguales en los dos proyectos; evaluación de
  las condiciones extraídas del JSON para las cuatro combinaciones de sensores:
  el rearme se acepta solo con entrada y salidas libres y se rechaza en las otras.
- Exportación y segunda exportación con tokens iguales excluyendo comentarios y
  espacios. Se conservaron texto, ZIP de ambos proyectos y resultados con hashes
  en `model/syson/importacion-corregida/`.
- Carga del ZIP desde Upload project: el servidor creó el proyecto y su contrato
  descargado por API coincide con el original. La espera de navegación automática
  del navegador agotó su tiempo; se registra separadamente del éxito de la carga.
- `uv run pytest -v`: 11 pruebas y 20 subpruebas aprobadas. Las vistas HTML
  mantienen el nombre del puerto y la misma condición lógica; no necesitaron cambios.

SysON sigue disponible en <http://localhost:8080>. El proyecto local
**OpenSort V1 corregido** tiene ID `6a9874e5-c744-4cd0-a6ac-b578656e239a`.
La referencia textual está corregida; no se acredita todavía ejecución del modelo
ni validación física. Los ZIP de esa evaluación no contienen diagramas; la entrega
posterior indicada a continuación añade y comprueba las representaciones.

## Vistas gráficas en SysON

El 2026-11-15, en `feature/syson-views`, se creó el proyecto independiente
**OpenSort V1 vistas**, sin sustituir los proyectos anteriores del usuario.
Las representaciones editables muestran componentes e interfaces (7 componentes,
12 puertos y 6 conexiones), ciclo de clasificación (15 nodos y 17 sucesiones) y
estados con rearme (3 estados y 5 transiciones visibles).

Se comprobó que el modelo original permanece igual al excluir únicamente los
`ViewUsage` añadidos. El ZIP recupera el documento con nuevos identificadores y
conserva las posiciones y tamaños de nodos, puertos y etiquetas. Las tres vistas
se abrieron en Chrome; los archivos y resultados están en
[`model/syson/vistas-v1/`](../model/syson/vistas-v1/README.md).

La reimportación del texto exportado terminó con informe vacío y conservó los
tres `ViewUsage`, las conexiones y los estados; creó cero representaciones
gráficas. Para recuperar los diagramas con su distribución se requiere el ZIP.

La comprobación en navegador de la copia recuperada terminó sin errores JavaScript.
Se verificaron los hashes de los archivos, la integridad de ambos ZIP, los enlaces
locales y `docker compose -f infra/syson/compose.yaml config --quiet`.

Son vistas seleccionadas: no dibujan los extremos implícitos `start`/`done` del
ciclo ni la entrada inicial de estados, que siguen presentes en el modelo.
La imagen de estados es una captura completa del navegador, porque la exportación
nativa recorta algunas etiquetas y bucles. El ZIP mantiene la vista editable.
No se cambió la simulación ni se acredita ejecución SysML o validación física.

Comprobaciones de cierre de la entrega conjunta: `uv run pytest -v` terminó con
11 pruebas y 20 subpruebas aprobadas; Compose validó su configuración y
`git diff --check origin/main...HEAD` no detectó errores de espacios. Se comprobaron
de nuevo la integridad de las exportaciones ZIP y los hashes de las vistas.

## Para retomar en otro chat

Compartir este archivo y el issue o hito a trabajar. Al cerrar una sesión, registrar aquí el último resultado comprobado y una siguiente acción concreta.
