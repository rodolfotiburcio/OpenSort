# Desarrollo de OpenSort con IA

Esta guía permite retomar el proyecto con contexto compartido y resultados
verificables. La configuración incluida está orientada a Codex. Con otros
asistentes, proporciona explícitamente `AGENTS.md` y las instrucciones de la skill
pertinente cuando no admitan su descubrimiento automático.

## Qué aporta cada pieza

| Pieza | Función en este proyecto | Ubicación |
|---|---|---|
| Instrucciones del repositorio | Contexto, reglas del dominio, comandos y forma de entregar | [AGENTS.md](../AGENTS.md) |
| Skills | Procedimientos reutilizables que se cargan según la tarea | [.agents/skills](../.agents/skills/) |
| Agentes especializados | Perfiles con una responsabilidad acotada para delegación explícita | [.codex/agents](../.codex/agents/) |
| MCP | Conexiones opcionales a documentación o GitHub | [Configuración](../.codex/config.toml) y [guía MCP](mcp.md) |
| Estado de sesión | Evidencia comprobada y siguiente acción para otro chat | [status.md](status.md) |
| ADR | Motivo, alcance y estado de una decisión de arquitectura | [docs/adr](adr/) |

Una skill describe cómo realizar una tarea. Un agente la lleva a cabo con las
herramientas disponibles. MCP conecta herramientas y datos externos; no instala
por sí mismo skills ni sustituye las pruebas del repositorio. Un plugin puede
agrupar skills y conexiones cuando haga falta distribuirlas entre proyectos.

## Empezar una sesión

Antes de editar, comprueba el árbol de trabajo y crea una rama para la tarea desde
la base actualizada. Por ejemplo, para un cambio independiente dirigido a `main`,
desde la raíz y con el árbol limpio:

```bash
git status --short
git fetch origin
git switch --no-track -c feature/mi-tarea origin/main
uv sync
codex
```

Sustituye `feature/mi-tarea` por un nombre descriptivo. Si hay cambios locales,
identifica a qué tarea pertenecen y consérvalos antes de cambiar de base. Si la tarea
ya tiene una rama, retómala. Antes del PR, revisa `git diff origin/main...HEAD`
y `git log --oneline origin/main..HEAD` para comprobar su alcance.

Codex descubre las skills de proyecto en `.agents/skills/`. Si no aparecen tras un
cambio, reinicia la sesión desde esta carpeta. Las instrucciones de `AGENTS.md`
se cargan al iniciar; no necesitas copiarlas en cada petición. Este comportamiento
se describe en las guías oficiales de [skills](https://developers.openai.com/codex/skills/)
y [AGENTS.md](https://developers.openai.com/codex/guides/agents-md/).

Primer mensaje sugerido:

```text
Lee AGENTS.md y docs/status.md. Comprueba la rama, los cambios locales y el código
relacionado con la siguiente tarea. Resume qué está implementado y qué falta.
Objetivo de esta sesión: [resultado concreto].
Criterio de aceptación: [comportamiento observable y cómo comprobarlo].
Implementa el cambio, verifica lo pertinente y registra el resultado comprobado.
```

Elige una tarea de la etapa actual. La hoja de ruta contiene tecnologías futuras;
su presencia allí no significa que estén instaladas o implementadas.

## Skills incluidas

| Skill | Cuándo usarla | Entrada |
|---|---|---|
| `opensort-simulator` | Clasificación, identidad, eventos, bloqueo y recuperación | [SKILL.md](../.agents/skills/opensort-simulator/SKILL.md) |
| `opensort-web` | Motor temporal, API, controles y representación 2D | [SKILL.md](../.agents/skills/opensort-web/SKILL.md) |
| `opensort-model` | Requisitos, SysML, vistas HTML y contrato de V1 | [SKILL.md](../.agents/skills/opensort-model/SKILL.md) |

Pueden seleccionarse automáticamente por su descripción o invocarse por nombre.
Por ejemplo, escribe en Codex:

```text
Usa $opensort-simulator para investigar este fallo: [pasos y resultado observado].
Corrígelo y añade una prueba que reproduzca la regresión.
```

```text
Usa $opensort-web para verificar que, después de un timeout, la cola permanece
detenida, el rearme exige una nueva pulsación y reanudar requiere iniciar alimentación.
Informa por separado las pruebas Python y la revisión visual.
```

```text
Usa $opensort-model para proponer el contrato del lector QR de V1. Enumera datos,
errores, decisiones pendientes y evidencia necesaria antes de elegir hardware.
```

Para añadir una skill, crea `.agents/skills/nombre/SKILL.md` con frontmatter YAML
`name` y `description`, seguido de instrucciones enfocadas en un trabajo repetible.
Usa `$skill-creator` si está disponible. Mantén las reglas generales en `AGENTS.md`
y la información específica en la skill. Comprueba que sus archivos referenciados
existen y ensáyala con una tarea real de su alcance.

## Agentes y reparto de trabajo

El agente principal puede implementar y verificar una tarea completa. Estos dos
perfiles están disponibles para pedir un análisis separado cuando sea útil:

| Perfil | Encargo | Resultado esperado |
|---|---|---|
| [opensort-reviewer](../.codex/agents/opensort-reviewer.toml) | Revisar un diff y sus pruebas | Defectos con ubicación, condición e impacto; lagunas de verificación |
| [opensort-model-analyst](../.codex/agents/opensort-model-analyst.toml) | Contrastar requisito, modelo, vistas y código | Discrepancias y propuesta de contrato con decisiones pendientes |

Los perfiles usan el modelo de la sesión principal y no se ejecutan por crearlos.
Piden trabajar sin editar; esa instrucción no crea un aislamiento de permisos.
Los subagentes heredan los permisos de la sesión. El formato de archivos TOML en
`.codex/agents/` corresponde a la [documentación actual de subagentes](https://developers.openai.com/codex/multi-agent/);
en clientes anteriores o con delegación deshabilitada, usa el mismo encargo con el
agente principal.

Ejemplo de delegación explícita:

```text
Delega en opensort-reviewer la revisión de los cambios locales de esta tarea.
Pídele que no edite archivos y que busque regresiones de bloqueo y rearme.
Espera su resultado, contrasta los hallazgos y corrige los defectos confirmados.
```

Al repartir trabajo, da a cada agente un objetivo, archivos de referencia, límites
de edición y criterio de cierre. Evita dos agentes editando el mismo archivo a la
vez; usa ramas o worktrees si necesitan cambios independientes. El agente principal
integra los resultados y verifica el conjunto. No se necesita delegación para cada
tarea ni los perfiles autorizan automáticamente publicaciones o acciones externas.

## Del pedido a una entrega comprobable

1. **Definir:** describe resultado esperado, entrada o evento que lo activa y
   criterio de aceptación. Usa datos sintéticos y enlaza el issue si existe.
2. **Investigar:** relaciona requisito, implementación y prueba; comprueba decisiones
   aceptadas y separa los supuestos que todavía faltan por confirmar.
3. **Implementar:** realiza el cambio acotado y actualiza representaciones afectadas.
4. **Verificar:** ejecuta las pruebas pertinentes. Para lógica o API, cierra con
   `uv run pytest -v`; para eventos CLI, ejecuta las demos; para vista, comprueba
   en navegador. Revisa `git diff --check` y el diff final.
5. **Entregar:** explica comportamiento, evidencia y pendientes. Actualiza el estado
   y, si cambia una decisión de arquitectura, añade un ADR con su estado.

Formato útil para una tarea o issue:

```text
Objetivo:
Situación actual y reproducción:
Comportamiento esperado:
Alcance / etapa:
Criterios de aceptación:
Fuentes o decisiones relacionadas:
```

La [plantilla de PR](../.github/pull_request_template.md) ayuda a conservar esa
evidencia. Una revisión de IA aporta hallazgos; la aceptación del cambio sigue
requiriendo contrastarlos con código, pruebas y criterios del proyecto.

## Mantener contexto y trazabilidad

`docs/status.md` guarda resultados y próximos pasos, evitando depender de una
conversación anterior. Registra las herramientas o skills realmente usadas cuando
ayude a reproducir el trabajo; no reconstruyas el historial previo por suposición.
El hecho de que estos archivos existan no demuestra que se usaron en versiones
anteriores del proyecto.

Para una decisión nueva, usa el siguiente número disponible en `docs/adr/` e incluye
estado, contexto, decisión, alternativas y consecuencias. No conviertas una
propuesta de la IA en una decisión aceptada sin evidencia de aceptación.

El código y los comandos locales bastan para trabajar en el simulador. Añade MCP
cuando una tarea necesite datos externos concretos; consulta [mcp.md](mcp.md) para
activar y comprobar únicamente la conexión correspondiente.
