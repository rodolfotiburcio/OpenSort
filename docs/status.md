# OpenSort — Estado del proyecto

Última actualización: 2026-11-12.

## Hito actual

V0 — Simulador de una estación logística implementado y validado localmente.
V1 — Modelo lógico de la estación de banco y visualización HTML integrados en `main` mediante el PR #2 (commit `2915aa4`). El rearme se añade en `model/opensort-v1-rearm`.

## Último resultado verificado

El lote de demostración de V0 confirma salidas, envía paquetes a revisión y bloquea la admisión ante una discrepancia. Las pruebas automatizadas cubren confirmación, causas de revisión, timeout, salida incorrecta y reprocesamiento. Consulta los [comandos de reproducción](../README.md#ejecutar).

El usuario confirmó que el [modelo SysML](../model/opensort.sysml) es correcto. El modelo documenta seis interfaces: detección de entrada, resultado QR, consulta y respuesta del manifiesto, orden de desvío, confirmación de salida y solicitud de rearme. La [vista HTML](estacion-v1.html) representa el ciclo, las interfaces y los estados de la estación; su actualización es manual.

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

Validar la ampliación SysML de estados y rearme en el visor utilizado y definir las interfaces físicas del banco: lector QR, sensores, botón y desviador.

## Pendientes posteriores

- Concretar pines, polaridades, filtrado, protocolos, formatos, tiempos y actuador.
- Definir la ubicación y el acceso al manifiesto.
- Integrar lector QR, ESP32, sensores y desviador; comprobar la política de manifiesto no disponible en la implementación.
- Validar la sintaxis de la ampliación SysML con una herramienta compatible e integrar la rama de rearme en `main`.
- Definir la secuencia de arranque y conectar las lecturas actuales de sensores y los eventos del ciclo a la máquina de estados.
- Implementar y probar el rearme en firmware/simulador: aceptación, rechazo, pulsación mantenida y conservación del resultado fallido.
- Publicar la visualización mediante GitHub Pages y evaluar su generación automática desde el modelo.

## Para retomar en otro chat

Compartir este archivo y el issue o hito a trabajar. Al cerrar una sesión, registrar aquí el último resultado comprobado y una siguiente acción concreta.
