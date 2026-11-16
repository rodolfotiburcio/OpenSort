# OpenSort — Estado del proyecto

Última actualización: 2026-11-15.

## Hito actual

V0 — Simulador de una estación logística implementado y validado localmente.
V1 — Modelo lógico de la estación de banco y visualización HTML integrados en `main` mediante el PR #2 (commit `2915aa4`). Los estados y el rearme están integrados mediante el PR #3 (`6ce304b`); la pizarra HTML navegable y la corrección del relleno de las flechas, mediante el PR #4 (`b952453`). El motor persistente, el rearme y la simulación 2D se integraron en `main` mediante el PR #5 (`4c45618`). La implementación física sigue pendiente.

La rama `feature/syson-local`, creada desde `origin/main` en `cc2e849`, incorpora
el entorno gráfico local SysON v2026.11.0 con Compose y PostgreSQL 15.20. El entorno
ya se ejecutó localmente. Esta rama todavía no está integrada en `main`.

`fix/syson-import`, basada en `feature/syson-local` (`a1fd901`), corrige la
importación y conserva conexiones, ciclo, estados y condiciones de rearme en la
exportación/reimportación. El archivo textual sigue siendo la referencia; la
creación y recuperación de representaciones gráficas se verifica por separado.

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

Revisar e integrar el entorno de `feature/syson-local` y su corrección dependiente
`fix/syson-import`. Después, crear las vistas de estructura, ciclo y estados en
SysON sobre los elementos existentes y comprobar que el ZIP conserva esas vistas.
La [evaluación corregida](../model/syson/importacion-corregida/README.md) documenta
la importación completa y el intercambio; la
[evaluación inicial](../model/syson/evaluacion-2026-11-15.md) se conserva como
histórico del fallo.

Tras verificar el modelo, concretar el contrato de hardware de V1: componentes,
pines, polaridades, filtrado, protocolos, tiempos, actuador y acceso al manifiesto,
antes de implementar firmware. La simulación ya está integrada en `main` mediante
el PR #5. Para reproducirla: `uv run opensort --web` (o `--port 8001`).

La simulación incorpora estados persistentes, cola, animación, sensores sintéticos, pausa y velocidad, fallos de salida y rearme mediante nueva pulsación. Once pruebas automatizadas cubren las reglas y la API local. La revisión automatizada en Chrome verificó las rutas A/B/C, revisión, timeout, rechazo y aceptación del rearme y pausa posterior, sin errores JavaScript ni desbordamiento horizontal en móvil. La simulación usa biblioteca estándar de Python y recursos web incluidos en el paquete, sin dependencias de ejecución adicionales.

Criterio de revisión: provocar un fallo, comprobar que la cola no se admite, rechazar rearme antes de inspeccionar o con sensores ocupados, aceptar otra pulsación tras despejar y reanudar explícitamente la alimentación. El historial debe conservar el fallo. La importación y reimportación del modelo ya se comprobaron en SysON v2026.11.0; su ejecución en un motor SysML y la validación física siguen pendientes.

## Pendientes posteriores

- Concretar pines, polaridades, filtrado, protocolos, formatos, tiempos y actuador.
- Definir la ubicación y el acceso al manifiesto.
- Integrar lector QR, ESP32, sensores y desviador; comprobar la política de manifiesto no disponible en la implementación.
- Crear y verificar las representaciones gráficas en SysON; conservarlas mediante exportación del proyecto completo.
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
ni validación física. Los ZIP de esta evaluación no contienen diagramas; el
siguiente paso sigue siendo crear y comprobar las representaciones indicadas arriba.

## Para retomar en otro chat

Compartir este archivo y el issue o hito a trabajar. Al cerrar una sesión, registrar aquí el último resultado comprobado y una siguiente acción concreta.
