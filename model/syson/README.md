# Intercambio de OpenSort con SysON

La referencia textual sigue en [`../opensort.sysml`](../opensort.sysml). Este
directorio conserva evidencia y exportaciones aceptadas del entorno
[SysON local](../../infra/syson/README.md); no contiene archivos de PostgreSQL.

La [evaluación inicial](evaluacion-2026-11-15.md) detectó una importación parcial.
La [corrección y nueva evaluación](importacion-corregida/README.md) recupera las
conexiones, `PackageCycle` y `StationStates`, y conserva las condiciones de rearme
al exportar y reimportar. Incluye texto, proyectos completos y resultados.

Las [vistas gráficas de V1](vistas-v1/README.md) añaden representaciones nativas
de componentes e interfaces, ciclo de clasificación y estados con rearme. Incluyen
el ZIP editable, exportación textual, imágenes y evidencia de recuperación.

Cuando se realice una evaluación o se acepte una versión, registrar:

- Versión de SysON y commit del modelo importado.
- Nombre del proyecto y fecha de evaluación.
- Informe de importación, incluidos errores y limitaciones.
- Resultado de revisar componentes, interfaces, ciclo y estados.
- Exportación `.sysml` y archivo completo `.zip` del mismo proyecto.
- Resultado de reimportar ambos en proyectos nuevos y diferencias observadas.

Guardar el texto exportado con otro nombre hasta comprobar su equivalencia; no
sobrescribir la referencia automáticamente. El ZIP conserva las representaciones
de SysON; el texto facilita la revisión en Git. Usar nombres con revisión o fecha,
datos sintéticos y solo exportaciones que aporten evidencia. Un arranque correcto
no acredita este intercambio.
