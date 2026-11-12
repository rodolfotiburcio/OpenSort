# Hoja de ruta de OpenSort

Plan de referencia de 24 semanas. Cada etapa cierra con una prueba reproducible y evidencia para GitHub y YouTube.

| Etapa | Semanas | Entrega | Criterio de cierre |
|---|---:|---|---|
| V0 — Simulación | 1–2 | Simulador Python, requisitos y flujo de eventos | Confirmar destinos, revisión y bloqueo ante discrepancias con datos sintéticos |
| V1 — Estación de banco | 3–8 | Banda, ESP32, lector QR, desviador y sensores; modelo SysML de interfaces y estados | Un paquete por ciclo; sensor confirma la salida y un atasco impide admitir el siguiente |
| V2 — Edge conectado | 9–14 | Gateway Linux, manifiesto versionado local, MQTT con mTLS, cola persistente, API y dashboard local | Clasificar con internet desconectado, recuperar eventos al reconectar y evitar duplicados |
| V3 — Plataforma cloud | 15–24 | Zonas y conductos OT, Tailscale, DMZ, AWS con Terraform, GitHub Actions, K3s, Traefik y TimescaleDB | Reproducir el despliegue, verificar flujos autorizados, restaurar un respaldo y mostrar la trazabilidad en el dashboard |
| Ampliación | Después de V3 | Encoder y seguimiento de varios paquetes simultáneos | Mantener la correspondencia entre identidad y posición, incluso ante errores de lectura |

Para cada episodio, enlaza desde el issue la versión demostrada, el comando de reproducción y el resultado observado. La primera demo puede mostrar la clasificación correcta, un QR desconocido y la banda simulada bloqueándose por una salida incorrecta.
