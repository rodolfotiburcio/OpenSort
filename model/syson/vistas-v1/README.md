# Vistas gráficas de OpenSort V1

Creación local del 2026-11-15 con SysON `v2026.11.0`, sobre
[`model/opensort.sysml`](../../opensort.sysml) del commit `2b8e6f2`.
Son representaciones editables de los elementos existentes: se añadieron tres
`ViewUsage` y sus exposiciones, sin cambiar componentes, conexiones ni reglas.
La referencia textual del repositorio sigue siendo la fuente principal.

## Abrir las vistas

En esta máquina está disponible el proyecto **OpenSort V1 vistas**:

| Vista | Abrir en SysON local | Contenido visible |
|---|---|---|
| Componentes e interfaces | [01 Componentes e interfaces](http://localhost:8080/projects/2d958ce9-4b4e-495d-8160-bd0e18dda527/edit/db5332d9-e86d-4d28-b8d1-fc16f60dcf87) | 7 componentes, 12 puertos y 6 conexiones |
| Ciclo de clasificación | [02 Ciclo de clasificación](http://localhost:8080/projects/2d958ce9-4b4e-495d-8160-bd0e18dda527/edit/5bd8da4a-6085-49c1-83a9-e63dc18a49a7) | 10 acciones, 4 decisiones, 1 unión y 17 sucesiones |
| Estados y rearme | [03 Estados y rearme](http://localhost:8080/projects/2d958ce9-4b4e-495d-8160-bd0e18dda527/edit/5953bfd4-7f1d-4baf-8167-6002ced7693e) | 3 estados y 5 transiciones con eventos, condiciones y efectos |

Los enlaces e identificadores corresponden a esta instancia. Para usar otra:

1. Inicia el [entorno local](../../../infra/syson/README.md).
2. En la página inicial, elige **Upload project** y carga
   [opensort-vistas.zip](opensort-vistas.zip).
3. Espera a que termine la carga del modelo y de sus representaciones. La aparición
   del nombre del proyecto en la lista no basta para darla por terminada.
4. Abre el proyecto y sus representaciones desde el Explorer. SysON asigna nuevos
   identificadores al recuperar el ZIP; los enlaces anteriores no apuntan a la copia.
5. Usa pantalla completa y **Fit to screen**. Haz clic en un espacio vacío antes
   de ajustar: con una selección activa se ajusta únicamente a esa selección.
   En estados, reduce el zoom si las etiquetas largas quedan fuera de pantalla.

Para continuar editando, usa una sola copia del proyecto y descarga de nuevo el
ZIP al entregar una revisión. Git no recoge los cambios del navegador.

## Archivos y comprobaciones

- [opensort-vistas.zip](opensort-vistas.zip): modelo y tres diagramas nativos,
  incluidos tamaños, posiciones, puertos y etiquetas ajustadas.
- [opensort-vistas.sysml](opensort-vistas.sysml): exportación textual separada,
  con las tres declaraciones `view` y sus exposiciones. No conserva la distribución
  gráfica del ZIP ni sustituye automáticamente la referencia.
- [restored-project.zip](restored-project.zip): segunda exportación del proyecto
  recuperado desde el ZIP, para contrastar la recuperación.
- [verification.json](verification.json): revisión de origen, hashes y resultados.
- [01-componentes.png](01-componentes.png) y [02-ciclo.png](02-ciclo.png):
  imágenes exportadas desde SysON.
- [03-estados.png](03-estados.png): captura de la vista recuperada en el navegador,
  con margen para las etiquetas y los bucles de transición.

Se comparó el JSON del modelo antes y después de crear las vistas, excluyendo
únicamente los nuevos `ViewUsage` y sus exposiciones: los elementos originales
permanecieron iguales. También se contrastaron las seis conexiones y las seis
transiciones del modelo, incluida la inicial. La recuperación compara el documento
tras normalizar los identificadores nuevos y las posiciones y tamaños de los nodos,
puertos y etiquetas por su identidad dentro de cada vista. Las tres representaciones
se abrieron en Chrome mediante Playwright temporal.

La reimportación del texto exportado terminó sin advertencias, conservó las
conexiones, las condiciones de estados y los tres `ViewUsage`, pero creó **cero
representaciones gráficas**. En esta versión, las declaraciones de vista del texto
no bastan para recuperar estos diagramas. Usa el ZIP para ese recorrido.

## Alcance de estas vistas

Son selecciones del modelo. El ciclo muestra desde `detectPackage` hasta
`recordConfirmedExit` o `blockAdmission`; no dibuja los extremos implícitos `start`
y `done`. La vista de estados no dibuja la entrada inicial a `available`.
Esos elementos siguen presentes en el modelo. Las ramas `else` del ciclo se muestran
sin texto en esta representación nativa; sus condiciones se conservan en el modelo.

La exportación nativa de imágenes de estados recortó etiquetas y bucles situados
fuera del rectángulo de los nodos. Por eso su imagen de consulta es una captura
completa del navegador. El ZIP conserva el diagrama editable.

Esta entrega comprueba creación, visualización e intercambio de representaciones.
No acredita ejecución del modelo en un motor SysML ni validación física.
