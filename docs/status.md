# OpenSort — Estado del proyecto

Última actualización: 2026-11-12.

## Hito actual

V0 — Simulador de una estación logística implementado y validado localmente.
V1 — Modelo lógico de la estación de banco y visualización HTML creados en la rama `model/opensort-v1-sysml`.

## Último resultado verificado

El lote de demostración de V0 confirma salidas, envía paquetes a revisión y bloquea la admisión ante una discrepancia. Las pruebas automatizadas cubren confirmación, causas de revisión, timeout, salida incorrecta y reprocesamiento. Consulta los [comandos de reproducción](../README.md#ejecutar).

El usuario confirmó que el [modelo SysML](../model/opensort.sysml) es correcto. El modelo documenta cinco interfaces: detección de entrada, resultado QR, consulta y respuesta del manifiesto, orden de desvío y confirmación de salida. La [vista HTML](estacion-v1.html) representa el ciclo y sus interfaces; su actualización es manual.

## Decisiones confirmadas

- Un paquete por ciclo, tres salidas de destino y una salida de revisión.
- Sin QR, QR ilegible (incluido timeout de lectura), ID desconocido o destino sin ruta: enviar a revisión.
- Manifiesto no encontrado o no disponible: enviar a revisión, igual que ante un QR ausente o ilegible. Esta política ya está reflejada en SysML y HTML.
- Toda salida, incluida revisión, requiere confirmación física.
- Una salida incorrecta o un timeout de confirmación bloquea la admisión del siguiente paquete.

## Siguiente tarea

Definir el rearme tras un bloqueo: quién lo solicita, qué condiciones deben comprobarse y cómo se registra el intento afectado antes de admitir otro paquete.

## Pendientes posteriores

- Concretar pines, polaridades, filtrado, protocolos, formatos, tiempos y actuador.
- Definir la ubicación y el acceso al manifiesto.
- Integrar lector QR, ESP32, sensores y desviador; comprobar la política de manifiesto no disponible en la implementación.
- Comprobar la vista HTML en navegador e integrar esta rama en `main`.
- Publicar la visualización mediante GitHub Pages y evaluar su generación automática desde el modelo.

## Para retomar en otro chat

Compartir este archivo y el issue o hito a trabajar. Al cerrar una sesión, registrar aquí el último resultado comprobado y una siguiente acción concreta.
