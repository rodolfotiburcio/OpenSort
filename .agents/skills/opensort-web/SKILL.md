---
name: opensort-web
description: Modificar o verificar la simulación 2D de OpenSort, su motor temporal, API HTTP y controles del navegador. Usar para opensort/web.py y opensort/static; no para crear dashboards de etapas futuras.
---

# Simulación web OpenSort

Lee `AGENTS.md`, `opensort/web.py`, los recursos afectados de `opensort/static/` y
`tests/test_web.py`. El motor Python es la fuente del estado; el navegador anima
una representación y envía comandos.

## Contratos relevantes

- `GET /api/state` entrega el estado; `POST /api/commands` recibe un objeto JSON
  con `action`. Conserva la validación de entradas y las respuestas de error.
- Servidor, reloj y peticiones comparten una `Simulation` protegida por un lock.
  Las pestañas comparten estación; recargar no reinicia y reiniciar el servidor sí.
- Conserva la escucha local en `127.0.0.1`. Una exposición a red cambia el alcance
  del servidor educativo y requiere un diseño específico.
- El navegador serializa comandos; pulsar y soltar rearme son eventos distintos.
  La pérdida de conexión deshabilita controles y no detiene el motor del servidor.
- La geometría y los sensores son sintéticos. La animación no prueba llegada física
  ni permite inferir que una estación real está despejada.

## Verificación

Para motor y API ejecuta `uv run pytest tests/test_web.py -v`; las pruebas crean
su propio servidor en un puerto libre. Para la vista inicia `uv run opensort --web`
y usa `--port 8001` si hace falta.

Comprueba en navegador lo que afecte el cambio: destinos A/B/C y revisión, pausa y
velocidad, bloqueo por timeout/salida incorrecta, rechazo de rearme sin inspección
o con sensor ocupado, nueva pulsación tras despejar y reanudación explícita. Si
cambias presentación, revisa ancho móvil, legibilidad y controles con teclado.

Informa por separado las pruebas Python y la comprobación visual realmente hecha.
Si no hay navegador disponible, indica el flujo visual pendiente. Detén el servidor
iniciado para la verificación al terminar.
