# SysON local para OpenSort

Entorno de modelado web con SysON `v2026.11.0` y PostgreSQL `15.20`, separado de
la simulación Python. Requiere Docker Engine y Docker Compose en ejecución.
Las imágenes incluyen las herramientas de ejecución: no se necesita instalar
Java ni Node.js en el host. La guía de SysON indica 4 GB de RAM disponibles y
recomienda 8 GB para su escenario de servidor pequeño; reserva espacio adicional
para imágenes, datos y respaldos.

## Iniciar desde la raíz del repositorio

```bash
docker compose -f infra/syson/compose.yaml config --quiet
docker compose -f infra/syson/compose.yaml up -d --wait --wait-timeout 180
docker compose -f infra/syson/compose.yaml ps
docker compose -f infra/syson/compose.yaml logs --tail 100 app
```

Abre <http://localhost:8080>. El primer arranque descarga las imágenes; la
aplicación puede tardar en inicializar aunque su contenedor figure en ejecución.
Ambos servicios deben estar `healthy`. Después del arranque comprueba la respuesta con:

```bash
curl --fail http://127.0.0.1:8080/ -o /dev/null
curl --fail http://127.0.0.1:8080/actuator/health
```

Solo se publica la aplicación en `127.0.0.1`; PostgreSQL permanece en la red
privada de Compose. No se configura autenticación para compartirlo en red:
este entorno es local, no un despliegue multiusuario ni de producción.

No incluye Elasticsearch ni su búsqueda entre proyectos. Desactivamos únicamente
su comprobación de salud opcional (`MANAGEMENT_HEALTH_ELASTICSEARCH_ENABLED=false`)
para que su ausencia no marque la aplicación como caída. Se conservan las demás
comprobaciones de salud, incluida PostgreSQL.

La configuración funciona con valores locales de ejemplo. Para cambiar el puerto
o la contraseña inicial, copia `infra/syson/.env.example` como `infra/syson/.env`
antes de crear la base y edita la copia. Compose carga ese archivo desde el
directorio del primer archivo Compose; las variables del shell prevalecen.
No publiques `.env`. Cambiar `SYSON_DB_PASSWORD` después de crear el volumen no
cambia la contraseña del usuario existente de PostgreSQL.

Para usar otro puerto sin crear `.env` (Bash):

```bash
SYSON_PORT=8081 docker compose -f infra/syson/compose.yaml up -d
```

Abre entonces <http://localhost:8081>. Las imágenes admiten amd64 y arm64.
Para instancias paralelas usa también `-p otro-nombre` en todos sus comandos:
el nombre del proyecto identifica contenedores, red y volumen.

## Detener y conservar el trabajo

```bash
docker compose -f infra/syson/compose.yaml down
docker compose -f infra/syson/compose.yaml up -d
```

El volumen `opensort-syson_database` conserva la base al recrear contenedores.
Su nombre cambia al usar `-p`. **`down -v` elimina el volumen y sus modelos**;
no se usa para detener una sesión. Un volumen no sustituye un respaldo.
No guardes archivos internos de PostgreSQL en Git.

Las tareas de `.vscode/tasks.json` ejecutan estos comandos desde la raíz. Se
encuentran en **Ejecutar tarea** y no inician servicios al abrir el editor.
La edición gráfica se realiza en el navegador.

## Evaluar nuestro modelo

`model/opensort.sysml` sigue siendo la referencia textual. No hay sincronización
con SysON ni generación de firmware o de las vistas HTML.

1. Crea un proyecto vacío, por ejemplo `OpenSort V1 evaluación`.
2. Usa **Upload model** en el Explorer e importa `model/opensort.sysml`. Si se
   añaden dependencias externas, impórtalas antes del documento que las usa.
3. Guarda y revisa el informe. Una importación parcial o referencias sin resolver
   no equivalen a un modelo validado, aunque se hayan creado elementos.
4. Contrasta `BenchStation`, sus seis interfaces, `PackageCycle` y `StationStates`.
   Verifica condiciones y acciones del rearme. Usa vistas de interconexión, flujo
   de acciones y transición de estados según corresponda.
5. Descarga el documento con nombre terminado en `.sysml` y guarda el resultado
   separado de la referencia. Descarga también el proyecto completo como ZIP:
   incluye modelos y representaciones en el formato JSON de SysON.
6. Reimporta texto y ZIP en proyectos nuevos y comprueba qué se conserva.
   Registra versión, informes, diferencias y resultado en `model/syson/README.md`.

Hasta comprobar ese recorrido no sustituimos el archivo original ni adoptamos
SysON como editor principal. Si se acepta después, cada entrega debe exportar
texto y proyecto completo para revisión en Git. Los cambios del navegador no hacen
commits; cambiar de rama Git no cambia el proyecto abierto en SysON. Identifica
la rama o revisión mediante los nombres de proyectos y exportaciones.

La [primera evaluación](../../model/syson/evaluacion-2026-11-15.md) detectó una
importación parcial. La [corrección posterior](../../model/syson/importacion-corregida/README.md)
permite importar sin advertencias y conservar las conexiones, el ciclo, los estados
y las condiciones de rearme al exportar y reimportar. Los proyectos de esa prueba
no tienen diagramas. La entrega posterior de [vistas gráficas de V1](../../model/syson/vistas-v1/README.md)
incluye las tres representaciones editables y su recuperación mediante **Upload project**.
Para abrirlas con su distribución, carga el ZIP de esa entrega desde la página
inicial; importar solamente `model/opensort.sysml` no reconstruye esos diagramas.

## Respaldo y restauración

Además del ZIP, antes de una actualización guarda un respaldo lógico.
Desde la raíz, en Bash y con los servicios iniciados:

```bash
mkdir -p infra/syson/backups
docker compose -f infra/syson/compose.yaml exec -T database pg_dump -U opensort -d opensort -Fc > infra/syson/backups/syson-before-upgrade.dump
```

Comprueba que `pg_dump` termine con código cero. Usa un nombre distinto para cada
respaldo que quieras conservar: la redirección sobrescribe el archivo indicado.
`infra/syson/backups/` está excluido de Git. Conserva otra copia fuera de la máquina
si necesitas recuperarte de una pérdida del disco.

Prueba la restauración en una **instancia nueva** con otro proyecto y puerto:

```bash
docker compose -p opensort-syson-restore -f infra/syson/compose.yaml up -d --wait database
docker compose -p opensort-syson-restore -f infra/syson/compose.yaml exec -T database pg_isready -U opensort -d opensort
docker compose -p opensort-syson-restore -f infra/syson/compose.yaml exec -T database pg_restore -U opensort -d opensort --no-owner --exit-on-error < infra/syson/backups/syson-before-upgrade.dump
SYSON_PORT=8081 docker compose -p opensort-syson-restore -f infra/syson/compose.yaml up -d app
```

Espera a que `pg_isready` termine correctamente antes de restaurar. La base de
destino debe estar vacía; si ya se usó ese proyecto, elige otro nombre. Comprueba
el resultado en <http://localhost:8081> y detén la copia con:

```bash
docker compose -p opensort-syson-restore -f infra/syson/compose.yaml down
```

Mantén la misma versión de SysON al restaurar. Para actualizar, respalda primero,
consulta las migraciones de la versión destino y ensaya en la copia. No reutilices
un volumen con otra versión mayor de PostgreSQL sin un procedimiento de migración.

## Fuentes y límites

- [Compose oficial v2026.11.0](https://github.com/eclipse-syson/syson/blob/v2026.11.0/docker-compose.yml): base de esta configuración; añadimos persistencia, espera de base y publicación local.
- [Instalación local](https://doc.mbse-syson.org/syson/v2026.11.0/installation-guide/how-tos/install/local_test.html) y [requisitos](https://doc.mbse-syson.org/syson/v2026.11.0/installation-guide/requirements.html).
- [Intercambio textual](https://doc.mbse-syson.org/syson/v2026.11.0/user-manual/features/import-export-textual.html): algunos conceptos siguen en desarrollo.
- [Gestión de proyectos](https://doc.mbse-syson.org/syson/v2026.11.0/user-manual/hands-on/how-tos/project-management.html) y [versionado externo](https://doc.mbse-syson.org/syson/v2026.11.0/user-manual/features/cm.html).
- [Notas de versión](https://doc.mbse-syson.org/syson/v2026.11.0/user-manual/release-notes/release-notes.html): una importación con errores de sintaxis puede ser parcial.
- [Elasticsearch opcional](https://doc.mbse-syson.org/syson/v2026.11.0/developer-guide/elasticsearch-integration.html) y [propiedades de salud de Spring Boot](https://docs.spring.io/spring-boot/appendix/application-properties/).

SysON es software abierto bajo EPL-2.0; sus componentes conservan sus licencias.
Incluir el Compose en este proyecto MIT no cambia esas licencias. Consulta
`docs/status.md` para saber qué comprobaciones se realizaron realmente.
