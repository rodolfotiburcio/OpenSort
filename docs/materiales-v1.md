# Materiales preliminares de V1

Estado: **borrador para seleccionar componentes y definir sus contratos físicos**.
Fecha: 2026-11-15.

Esta lista parte del [modelo lógico](../model/opensort.sysml), la
[hoja de ruta](roadmap.md) y las [decisiones de V1](status.md#decisiones-confirmadas).
Todavía no fija referencias comerciales, precios, pines ni valores eléctricos o
mecánicos. Las cantidades indicadas como propuestas se revisarán al elegir el
mecanismo y las dimensiones de la estación; no constituyen una lista de compra cerrada.

## Componentes vinculados al modelo

Los nombres de la columna «Elemento SysML» pertenecen a `OpenSort::BenchStation`.
La familia ESP32 ya está prevista en el modelo; la placa y su revisión siguen
pendientes. En todas las filas está pendiente seleccionar y documentar la solución física.

| ID | Componente o recurso y función | Cantidad preliminar | Elemento SysML | Parámetros por definir |
|---|---|---|---|---|
| MAT-01 | Placa controladora ESP32: coordinar lectura, clasificación, bloqueo y rearme | 1 | `controller` | Placa y revisión; alimentación y consumo; GPIO disponibles y restricciones de arranque; asignación de pines; niveles eléctricos; entradas/salidas necesarias; interfaces de comunicación; programación y depuración. |
| MAT-02 | Sensor de entrada: detectar el paquete e iniciar un intento cuando la estación esté disponible | 1 punto de detección | `entrySensor` | Tecnología; alcance y tamaño mínimo detectable; ubicación; alimentación; tipo y nivel de salida; polaridad; pin; filtrado y tiempo mínimo de detección; criterio de sensor libre. |
| MAT-03 | Lector QR: entregar el identificador del paquete | 1 | `qrReader` | Modelo; interfaz eléctrica y protocolo; alimentación y consumo; formato y delimitación de mensajes; disparo de lectura; distancia, orientación e iluminación; tamaño de etiqueta; plazo de lectura y tratamiento de ausencia, error o timeout. |
| MAT-04 | Mecanismo desviador y sus actuadores: conducir el paquete a la salida ordenada | 1 conjunto; número de actuadores por definir | `diverter` | Geometría para tres destinos y revisión; tipo y cantidad de actuadores; fuerza o par; carrera o ángulos; alimentación y corriente; etapa de mando; señales y pines; posiciones y calibración; tiempo de movimiento y estabilización; necesidad de realimentación. |
| MAT-05 | Sensores de salida: observar por dónde salió realmente el paquete | 4 puntos de detección; propuesta de un sensor por salida | `exitSensors` | Tecnología y modelo; ubicación en cada salida; alimentación y salida eléctrica; polaridad; pines; filtrado; correspondencia sensor–salida; plazo de confirmación; tratamiento de señales simultáneas y criterio de salidas libres. |
| MAT-06 | Pulsador físico de rearme: emitir una nueva solicitud después de inspeccionar y despejar | 1 | `resetButton` | Tipo de contacto; montaje; alimentación o referencia eléctrica; polaridad y resistencias de polarización; pin; antirrebote; detección de nueva pulsación y liberación; comportamiento ante botón mantenido. |
| REC-01 | Fuente del manifiesto: resolver `package_id` a destino y comunicar indisponibilidad | 1 fuente lógica; hardware adicional por decidir | `manifestSource` | Ubicación del archivo o servicio; formato; carga del lote; transporte y protocolo; interfaz con ESP32; plazos de consulta; respuesta para ID desconocido o fuente no disponible; tabla destino–salida. Puede reutilizar hardware existente. |

Los cuatro puntos de salida incluyen `exit1`, `exit2`, `exit3` y `review`.
La cantidad final de dispositivos de detección depende de la solución elegida.
La orden enviada al desviador no sustituye la observación independiente de salida.

## Materiales de soporte propuestos

Estos conjuntos desarrollan la estación física prevista en la hoja de ruta.
Aún no están desglosados como piezas en `BenchStation`; incorporarlos al modelo
detallado y asignarles requisitos será parte del diseño físico. Las cantidades
son propuestas, no decisiones de arquitectura aceptadas.

| ID | Material o conjunto | Cantidad preliminar | Parámetros por definir |
|---|---|---|---|
| MAT-07 | Banda transportadora, rodillos y tensor | 1 conjunto | Longitud y ancho útiles; material y superficie; dimensiones y masa de paquetes admitidos; velocidad; separación entre paquetes; diámetros de rodillos; recorrido y ajuste del tensor. |
| MAT-08 | Motor de transporte y transmisión | 1 conjunto propuesto | Tipo de motor; alimentación; corriente nominal y de arranque; velocidad y par requeridos; reducción; acoplamiento; fijación; necesidad de medir velocidad o posición. |
| MAT-09 | Etapa de potencia del motor | 1 por motor, por confirmar | Compatibilidad con el motor; tensión y corriente; señales de habilitación y velocidad; niveles lógicos; pines; disipación; frenado o parada; comportamiento al arrancar el controlador. |
| MAT-10 | Etapas de mando de los actuadores del desviador | Según MAT-04; pueden estar integradas | Tipo de actuador compatible; canales; alimentación y corriente; interfaz con ESP32; pines; disipación; estado al encender y ante pérdida de mando. Evitar contarlas dos veces si el conjunto ya las incluye. |
| MAT-11 | Fuentes de alimentación y reguladores | Según tensiones y cargas elegidas | Tensiones de distribución; balance de consumo y arranque; capacidad de corriente; conversión; separación entre lógica y potencia; filtrado; conexión de referencias eléctricas; conectores. |
| MAT-12 | Distribución eléctrica, protecciones y mandos de alimentación/parada | 1 conjunto por dimensionar | Esquema de alimentación; ramales; protecciones y calibres; seccionamiento; comportamiento de parada y recuperación; relación con el control. El pulsador de rearme conserva su función específica. |
| MAT-13 | Adaptación y acondicionamiento de señales | Según sensores, lector y etapas elegidos | Compatibilidad de niveles; adaptación o aislamiento requerido; resistencias; filtros; polaridades; retardos introducidos; esquema por canal. |
| MAT-14 | Bastidor, soportes, guías y resguardos | 1 conjunto | Materiales; dimensiones; rigidez; fijación al banco; accesibilidad; separación de mecanismos; soportes de sensores y lector; tolerancias y método de fabricación. |
| MAT-15 | Canales o recipientes de salida | 4 puntos de recepción | Geometría; capacidad; identificación de destinos y revisión; posición de sensores; retirada de paquetes y acceso para despejar la estación. |
| MAT-16 | Placa de interconexión, borneras, conectores y cableado | Según esquema y montaje | Número de señales y ramales; secciones y longitudes; conectores y pinout; sujeción; separación de potencia y señales; identificación; acceso para medir y mantener. |
| MAT-17 | Caja o panel para electrónica y mandos | 1 conjunto propuesto | Dimensiones; distribución; ventilación; montaje de placa, etapas y fuentes; acceso a programación; entradas de cables y fijación del pulsador. |
| MAT-18 | Tornillería, separadores y piezas de montaje | Según planos | Diámetros; longitudes; material; cantidad por unión; piezas impresas o mecanizadas; compatibilidad con soportes y tolerancias. |
| AUX-01 | Paquetes y etiquetas QR de prueba | 1 lote sintético | Dimensiones y masas de ensayo; material y posición de etiquetas; IDs conocidos y desconocidos; casos sin QR o ilegibles; destino asociado en el manifiesto. |

El PC de desarrollo, el cable de programación, los instrumentos de medida y las
herramientas de montaje se registrarán como medios de trabajo disponibles o por
conseguir. No se presupone que formen parte permanente de la estación. REC-01
debe resolverse antes de decidir si V1 necesita otro equipo de cómputo; el gateway
y la sincronización previstos para V2 no se añaden automáticamente a esta lista.

## Contratos que deben acompañar la selección

Cada pieza elegida debe registrar referencia exacta, revisión, cantidad final y
hoja de datos o plano de origen. Los valores eléctricos y mecánicos se fijarán
con esa evidencia. El esquema y el mapa de pines deben identificar los extremos
de cada conexión y los acondicionamientos intermedios.

| Interfaz del modelo | Filas relacionadas | Decisiones que deben quedar documentadas |
|---|---|---|
| `EntrySignal` | MAT-01, MAT-02, MAT-13 | Pin, nivel activo, filtrado y evento de detección; lectura actual usada para determinar entrada libre. |
| `QrSignal` | MAT-01, MAT-03 | Conexión, protocolo, mensaje con `package_id`, disparo y plazo de lectura; resultado ilegible si falta QR o vence el plazo. |
| `ManifestAccess` | MAT-01, REC-01 | Transporte, formato de consulta y respuesta, plazos, ID desconocido e indisponibilidad. El QR contiene identidad; el manifiesto resuelve destino y la tabla de rutas resuelve salida. |
| `DivertSignal` | MAT-01, MAT-04, MAT-10 | Mando por salida, posiciones y calibración; tiempo de posicionamiento y estabilización. |
| `ExitSignal` | MAT-01, MAT-05, MAT-13 | Pin y polaridad por sensor, filtrado, salida observada y plazo de confirmación. Salida incorrecta o timeout bloquean la admisión. |
| `ResetSignal` | MAT-01, MAT-06 | Pin, polaridad, antirrebote y nueva pulsación. Solo se acepta estando bloqueado, tras inspección y con entrada y salidas libres; conserva el fallo y no inicia movimiento. |

Además de esos seis contratos, falta detallar el mando del transporte, la
secuencia de arranque y las respuestas físicas ante bloqueo o parada. El modelo
lógico actual describe el bloqueo de admisión; no fija por sí solo todas las
acciones eléctricas y mecánicas de la estación.

## Orden para completar la lista

1. Definir el rango de paquetes, las dimensiones del banco y la velocidad de
   trabajo; elegir el principio mecánico para llegar a las cuatro salidas.
2. Seleccionar banda, motor y actuadores, y cerrar su alimentación y etapas de mando.
3. Seleccionar lector, sensores, placa ESP32 y pulsador; comprobar conjuntamente
   interfaces, entradas/salidas disponibles y acondicionamiento de señales.
4. Resolver REC-01, completar el mapa de pines, los esquemas y los plazos del ciclo.
5. Registrar las decisiones aceptadas, actualizar las partes afectadas del modelo
   y comprobar los contratos en banco antes de dar por validada la implementación física.

El seguimiento de la tarea está en [estado del proyecto](status.md#siguiente-tarea).
Las [vistas de SysON](../model/syson/vistas-v1/README.md) representan el modelo
lógico disponible; esta lista no modifica sus conexiones ni sus estados.
