# ADR 001 — El QR identifica al paquete

**Estado:** aceptada para V0.

La estación necesita clasificar paquetes por destino, permitir cambios de asignación sin reimprimir etiquetas y, en una etapa posterior, operar con un manifiesto local aunque pierda internet.

El QR contiene el identificador del paquete. El manifiesto del lote resuelve el destino y una tabla de rutas relaciona el destino con la salida. V0 usa una copia en memoria. La sincronización y el versionado del manifiesto corresponden a V2.

Cada paso físico tiene un identificador de intento propio, emitido como `attempt_id`. Un paquete reprocesado conserva el mismo `package_id` y adquiere otro intento. Un paquete desconocido, ilegible o sin ruta asignada se dirige a revisión. Su llegada a revisión también se confirma mediante una observación de salida.
