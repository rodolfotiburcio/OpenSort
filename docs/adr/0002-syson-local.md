# ADR 002 — Entorno local de modelado con SysON

**Estado:** aceptada para integrar el entorno local. La importación, exportación
y recuperación del modelo lógico de V1 y sus vistas se comprobaron en v2026.11.0.
La adopción de SysON como editor principal queda pendiente de una decisión explícita
sobre el flujo de edición; la referencia textual se conserva.

## Contexto

OpenSort mantiene un modelo textual SysML v2 y vistas HTML manuales. Se necesita
un entorno gráfico abierto que pueda recrearse desde el repositorio sin añadir
dependencias al simulador Python. El usuario eligió evaluar SysON v2026.11.0 con
Docker Compose y autorizó su integración en una rama independiente.

## Decisión

- Versionar el entorno en `infra/syson/`, con SysON v2026.11.0 y PostgreSQL 15.20.
- Conservar la base en un volumen, publicar la aplicación en loopback y esperar a
  que PostgreSQL esté disponible antes de iniciarla.
- Mantener VS Code como editor del repositorio; usar el navegador para SysON.
- Conservar `model/opensort.sysml` como referencia; el intercambio comprobado no
  cambia automáticamente la fuente principal de edición.
  Importar en proyectos de evaluación y revisar informes y elementos del modelo.
- Para una entrega aceptada, conservar texto y archivo completo de proyecto con
  sus representaciones. Git no se sincroniza automáticamente con SysON.
- Documentar respaldo lógico y restauración en otra instancia antes de actualizar.
- Añadir el skill `opensort-syson` para este flujo repetible. Los perfiles existentes
  cubren el análisis del modelo; no se añade otro agente por ahora.

## Alternativas

Instalar SysON directamente exige mantener herramientas de ejecución en cada host.
Un servidor compartido requiere decisiones adicionales de acceso, operación y
respaldo. Mantener solo texto y HTML evita esos servicios, pero no ofrece la edición
gráfica elegida. Empezamos con Compose local para evaluar el modelo existente.

## Consecuencias

El entorno requiere Docker, memoria y disco adicionales; la simulación funciona
sin ellos. El volumen facilita continuidad local; las exportaciones y respaldos
permiten recuperar versiones. La compatibilidad de estados, acciones y conexiones
con el importador debe comprobarse: levantar SysON no valida por sí solo la sintaxis
ni el comportamiento físico de OpenSort.

Referencias y comandos: [guía de SysON local](../../infra/syson/README.md).
Evidencia del intercambio: [importación corregida](../../model/syson/importacion-corregida/README.md)
y [vistas gráficas recuperadas](../../model/syson/vistas-v1/README.md).
