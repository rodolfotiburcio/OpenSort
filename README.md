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

## Continuar el proyecto

- [Estado y siguiente tarea](docs/status.md)
- [Hoja de ruta](docs/roadmap.md)
- [Modelo y criterios de V0](docs/simulator.md)
- [ADR 001 — Identidad y destino del paquete](docs/adr/0001-qr-package-id.md)

El código y la documentación se publican bajo la [licencia MIT](LICENSE).
