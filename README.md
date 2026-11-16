# OpenSort IIoT

Proyecto educativo para construir una estación logística que clasifica paquetes por destino. Cada QR identifica un paquete. La estación consulta el destino en el manifiesto del lote, elige una salida y registra el resultado después de observar por dónde pasó el paquete.

La V0 simula una estación con tres salidas de destino y una de revisión. Procesa un paquete por ciclo. El lector QR y los sensores se representan con entradas sintéticas.

## Ejecutar

El proyecto usa [uv](https://docs.astral.sh/uv/) para gestionar el entorno y las dependencias. Desde la raíz del repositorio:

```bash
uv sync                                  # crea .venv e instala dependencias (incluye pytest)
uv run opensort                          # ejecuta la demostración
uv run opensort --scenario wrong-exit
uv run pytest -v                         # ejecuta las pruebas
```

El paquete no tiene dependencias externas en tiempo de ejecución; pytest solo se usa para desarrollo. Requiere Python 3.10 o superior (uv lo descarga si hace falta). También funciona `uv run python -m opensort`.

La demostración emite un objeto JSON por evento. En el escenario predeterminado se confirman dos paquetes, tres pasan a revisión y el siguiente causa un bloqueo por falta de confirmación. El último paquete del lote queda pendiente. El segundo escenario sustituye el timeout por una salida incorrecta.

## Simulación 2D interactiva

```bash
uv run opensort --web                     # servidor local en http://127.0.0.1:8000
uv run opensort --web --port 8001         # alternativa si el puerto está ocupado
```

Abre la dirección indicada en el navegador. Añade paquetes a la cola o carga el lote de demostración y pulsa **Iniciar alimentación**. La vista muestra banda, lector QR, desviador, tres salidas de destino y revisión. Puedes pausar, cambiar la velocidad y preparar intentos con salida incorrecta, timeout o manifiesto no disponible. El lote de demostración incluye un timeout y deja un paquete pendiente.

Tras un fallo, la estación permanece bloqueada. Confirma la inspección y el despeje, comprueba los sensores y pulsa rearme. Para probar un rechazo, marca algún sensor como ocupado. Después de liberarlo se requiere otra pulsación. El rearme conserva el fallo y no inicia movimiento: pulsa **Iniciar alimentación** para continuar.

El motor y los tiempos se ejecutan en Python; el navegador dibuja su estado. Las pestañas comparten una estación en memoria: recargar conserva la sesión, reiniciar el servidor la borra. Si se pierde la conexión se deshabilitan los controles; el motor del servidor sigue su estado actual. La geometría es ilustrativa, con un paquete por ciclo y sin conexión a hardware. Usa `Ctrl+C` en la terminal para detener el servidor.

## Continuar el proyecto

- [Estado y siguiente tarea](docs/status.md)
- [Hoja de ruta](docs/roadmap.md)
- [Modelo y criterios de V0](docs/simulator.md)
- [ADR 001 — Identidad y destino del paquete](docs/adr/0001-qr-package-id.md)

El código y la documentación se publican bajo la [licencia MIT](LICENSE).
