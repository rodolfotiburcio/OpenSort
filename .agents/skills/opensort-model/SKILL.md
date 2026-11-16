---
name: opensort-model
description: Revisar o actualizar la coherencia de requisitos, interfaces y estados de OpenSort entre SysML, vistas HTML, simulador y ADR. Usar para modelado y contratos de V1; no para afirmar validación física o sintáctica sin herramientas y evidencia.
---

# Modelo y contratos OpenSort

Consulta `AGENTS.md`, `docs/status.md`, `docs/roadmap.md`,
`docs/adr/0001-qr-package-id.md`, `model/opensort.sysml` y las secciones afectadas de
`docs/estacion-v1.html` y `docs/pizarra-v1.html`.

## Revisión del contrato

Relaciona cada requisito cambiado con su interfaz, transición y evidencia en código
o prueba. Distingue el modelo lógico de V1, la simulación implementada y las funciones
planificadas para V2/V3. Las dos vistas HTML se actualizan manualmente.

Conserva las seis interfaces documentadas: detección de entrada, resultado QR,
consulta/respuesta del manifiesto, orden de desvío, observación de salida y solicitud
de rearme. El botón representa una nueva pulsación después de inspeccionar; sensores
libres, por sí solos, no prueban que toda la estación esté despejada.

Si se pide concretar hardware, identifica las decisiones pendientes: pines,
polaridades, filtrado, protocolo del lector, ubicación del manifiesto, actuador y
tiempos. Registra supuestos como propuestas; apóyate en hojas de datos oficiales
para el componente y revisión elegidos antes de fijar valores.

## Entrega

Al editar un contrato, actualiza sus representaciones afectadas y explica cualquier
diferencia intencional con el simulador. Registra decisiones nuevas en `docs/adr/`
con su estado y actualiza `docs/status.md` cuando corresponda.

Revisa enlaces y abre las vistas HTML si cambias su presentación. Ejecuta las
pruebas Python si cambian reglas implementadas. Una inspección textual no valida la
sintaxis SysML: solo declara esa validación si ejecutaste una herramienta compatible,
indicando cuál y el resultado. La comprobación física requiere evidencia de banco.
