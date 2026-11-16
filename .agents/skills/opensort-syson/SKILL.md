---
name: opensort-syson
description: Configurar, ejecutar o depurar SysON local de OpenSort con Docker Compose y gestionar la importación, exportación y recuperación de modelos. Usar para infra/syson y su flujo de trabajo; las reglas de clasificación corresponden a opensort-simulator.
---

# SysON de OpenSort

Lee `infra/syson/README.md`, `docs/adr/0002-syson-local.md` y el estado de
verificación en `docs/status.md`. El proyecto Compose es `opensort-syson`;
comprueba si ya está en uso antes de iniciar o detener servicios. Para pruebas
temporales usa otro nombre con `-p` y otro `SYSON_PORT`, conservando su volumen.

## Entorno y datos

El Compose fija las imágenes y espera a PostgreSQL. La base tiene un volumen
persistente y no publica puerto. Conserva el acceso local de la aplicación.
El simulador Python no depende de estos servicios.

Antes de actualizar imágenes, guarda una exportación del proyecto y un respaldo
de la base según la guía. Un volumen conserva datos entre recreaciones, pero no
reemplaza un respaldo. No uses `down -v`, limpieza global de Docker ni modifiques
tablas internas para editar el modelo. Una contraseña de `.env` solo inicializa
PostgreSQL cuando el volumen está vacío.

## Modelo y versiones

Mientras no se verifique el intercambio completo, `model/opensort.sysml` sigue
siendo la referencia textual y SysON se usa como entorno de evaluación. Importa
en un proyecto nuevo y revisa el informe: un éxito HTTP puede incluir una
importación parcial. Comprueba especialmente `BenchStation`, `PackageCycle` y
`StationStates`, sus conexiones, condiciones y acciones de rearme.

Exporta texto a un archivo separado y el proyecto completo como ZIP con sus
representaciones; registra versión de SysON, origen, informes y resultado de
reimportación en `model/syson/README.md` cuando haya evidencia. No sobrescribas la
referencia ni declares sincronización automática o validación sintáctica completa
por el mero hecho de abrir la página. No edites simultáneamente dos copias como
fuentes principales. Para cambiar contratos aplica también `opensort-model`.

## Comprobación

Ejecuta `docker compose -f infra/syson/compose.yaml config --quiet`. Si Docker
está disponible, verifica arranque, respuesta HTTP y conservación de un proyecto
tras `down` y `up`; informa por separado las pruebas de importación/exportación
y restauración realmente realizadas. Documenta las limitaciones sin convertir
un fallo de importación en permiso para reescribir el modelo o actualizar SysON.
