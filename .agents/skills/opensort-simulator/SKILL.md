---
name: opensort-simulator
description: Modificar o depurar la clasificación, los eventos y la recuperación del simulador OpenSort. Usar para reglas de dominio y regresiones; los cambios puramente visuales corresponden a opensort-web.
---

# Simulador OpenSort

Lee `AGENTS.md`, `opensort/simulator.py`, `tests/test_simulator.py` y las pruebas
de `RecoveryTests` en `tests/test_web.py`. Consulta el ADR 001 si cambia la identidad
del paquete, el manifiesto o la ruta.

## Decisiones que deben conservarse

- `Station.start()` admite solo en `available`; mientras procesa o está bloqueada
  no debe crear otro intento. `finish()` recibe una observación independiente.
- `Station.run()` se detiene ante un bloqueo. Una llamada posterior no lo borra.
- Un resultado `sent_to_review` tiene confirmación de llegada a revisión;
  `station_blocked` registra timeout o discrepancia, aunque la ruta fuera revisión.
- `failed` conserva el resultado fallido después de un rearme aceptado. El evento
  de rearme no debe sustituir el resultado original en el historial.
- El flanco del botón y la pausa tras el fallo pertenecen a `Simulation` en
  `opensort/web.py`; probar `Station.reset()` por sí solo no verifica ese contrato.

## Trabajo y evidencia

Reproduce la transición afectada con entradas sintéticas. Cuando cambie una regla,
añade una prueba del resultado observable: eventos, identificadores, estado o
admisión del siguiente paquete. Incluye el caso de revisión si cambias confirmación
o bloqueo y el reprocesamiento si cambias identidad.

Ejecuta `uv run pytest tests/test_simulator.py tests/test_web.py -v`. Comprueba las
demos `uv run opensort` y `uv run opensort --scenario wrong-exit` si cambian eventos
o su formato. Los UUID varían: compara relaciones entre intentos, no valores fijos.

Entrega el comportamiento anterior y nuevo, la evidencia ejecutada y las decisiones
de dominio que necesiten actualizar modelo o documentación.
