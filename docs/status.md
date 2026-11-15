# OpenSort — Estado del proyecto

Última actualización: 2026-11-14.

## Hito actual

V0 — Simulador de una estación logística implementado y validado localmente.
V1 — Modelo lógico de la estación de banco y visualización HTML integrados en `main` mediante el PR #2 (commit `2915aa4`). Los estados y el rearme están integrados mediante el PR #3 (`6ce304b`); la pizarra HTML navegable y la corrección del relleno de las flechas, mediante el PR #4 (`b952453`). La implementación física y el rearme en código siguen pendientes.

## Último resultado verificado

El lote de demostración de V0 confirma salidas, envía paquetes a revisión y bloquea la admisión ante una discrepancia. Las pruebas automatizadas cubren confirmación, causas de revisión, timeout, salida incorrecta y reprocesamiento. Consulta los [comandos de reproducción](../README.md#ejecutar).

En la revisión local pasaron las cuatro pruebas con `python3 -m unittest discover -s tests -v` y se verificó la demo `python3 -m opensort --scenario wrong-exit`. El bloqueo actual solo detiene el lote de una llamada a `Station.run()`; no persiste entre llamadas y todavía no exige rearme para volver a procesar paquetes.

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

Implementar y probar en el simulador los estados persistentes de la estación (disponible, procesando y bloqueada) y el rearme definido en el modelo V1.

Criterio de cierre: provocar un fallo, impedir la admisión de otro paquete incluso en una nueva llamada, rechazar el rearme con algún sensor ocupado, aceptar una nueva pulsación con todos los sensores libres y procesar otro paquete. Verificar también que una pulsación mantenida o anterior al bloqueo no produce rearme automático, que fuera del bloqueo se ignora el rearme y que se conserva el resultado fallido sin iniciar movimiento al rearmar.

## Pendientes posteriores

- Concretar pines, polaridades, filtrado, protocolos, formatos, tiempos y actuador.
- Definir la ubicación y el acceso al manifiesto.
- Integrar lector QR, ESP32, sensores y desviador; comprobar la política de manifiesto no disponible en la implementación.
- Validar la sintaxis de la ampliación SysML de estados y rearme con una herramienta compatible.
- Definir la secuencia de arranque y conectar las lecturas actuales de sensores y los eventos del ciclo a la máquina de estados.
- Tras validar el simulador, implementar y probar el rearme en firmware con sensores y botón físicos.
- Publicar la visualización mediante GitHub Pages y evaluar su generación automática desde el modelo.

## Para retomar en otro chat

Compartir este archivo y el issue o hito a trabajar. Al cerrar una sesión, registrar aquí el último resultado comprobado y una siguiente acción concreta.
