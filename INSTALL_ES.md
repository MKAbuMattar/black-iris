# Instalar black-iris

Una sola carpeta de habilidad, `skills/black-iris/`, funciona en cualquier
agente que lea Agent Skills. Todas las rutas de abajo terminan en lo mismo: esa
carpeta, con sus referencias, en un lugar que tu agente escanea. Solo Claude
Code recibe ademas el hook SessionStart; el resto recibe la habilidad y puede
anadir a mano un fragmento siempre activo.

Los comandos asumen que el repositorio esta publicado en
`github.com/MKAbuMattar/black-iris`. Hasta que se publique, usa las rutas de
ruta local.

Lo que comparten todas las rutas:

- Invoca por nombre. `/black-iris` donde existan habilidades con barra,
  `$black-iris` en Codex, o pidelo con palabras. Shape, Build y la Cut list
  siguen activos hasta "stop black-iris" o "normal mode".
- Los archivos por proyecto van a `~/.BLACK_IRIS_AGENTS/projects/<slug>/`.
  Nada se escribe en tu repositorio ni en `~/.claude`.
- Indicador siempre activo:
  `mkdir -p ~/.BLACK_IRIS_AGENTS && touch ~/.BLACK_IRIS_AGENTS/always-on`.
  Solo la ruta de plugin de Claude Code lo lee.

## Claude Code

Ruta de plugin, da la habilidad y el hook:

```bash
claude plugin marketplace add MKAbuMattar/black-iris
claude plugin install black-iris@black-iris
```

Ruta de plugin local, sin publicar, una sesion a la vez:

```bash
claude --plugin-dir /ruta/a/black-iris
```

Ruta solo habilidad, sin hook:

```bash
python3 skills/black-iris/scripts/universal/install.py               # enlace en ~/.claude/skills
python3 skills/black-iris/scripts/universal/install.py --always-on   # ademas fija el indicador
python3 skills/black-iris/scripts/universal/install.py --uninstall
```

`scripts/linux/install.sh`, `scripts/mac/install.sh` y
`scripts/windows/install.ps1` hacen lo mismo en la shell de cada plataforma.

Verificar: abre una sesion nueva y escribe `/black-iris`, o ejecuta
`claude plugin list`. Actualizar: `claude plugin marketplace update black-iris`.
Desinstalar: `claude plugin uninstall black-iris` y luego
`claude plugin marketplace remove black-iris`.

Con el indicador puesto y el plugin cargado, cada inicio, reanudacion,
limpieza y compactacion de sesion reinyecta el cuerpo de la habilidad, las
nueve referencias y el `MEMORY.md` del proyecto, unas 1.700 lineas. Sin el plugin, el indicador no hace nada.

Claude for IDE (las extensiones de VS Code y JetBrains) ejecuta el mismo
Claude Code por debajo y lee los mismos `~/.claude/skills` y lista de plugins.
Cualquier ruta de arriba lo cubre; abre un chat nuevo en el IDE tras instalar.

## Codex

```bash
codex plugin marketplace add MKAbuMattar/black-iris --ref main
codex plugin add black-iris@black-iris
```

El repositorio incluye `.codex-plugin/plugin.json` y un archivo de marketplace
de Codex en `.agents/plugins/marketplace.json`, que es lo que lee el primer
comando. Escribe `$black-iris`. La habilidad permite invocacion implicita, asi que Codex
tambien puede activarla desde la descripcion. Alternativa solo habilidad:

```bash
npx skills add MKAbuMattar/black-iris -a codex        # o copia skills/black-iris a ~/.codex/skills/
```

Actualizar: `codex plugin marketplace upgrade black-iris`, luego quitar y
anadir. Desinstalar: `codex plugin remove black-iris` y
`codex plugin marketplace remove black-iris`. Siempre activo: pega el
fragmento del final en `~/.codex/AGENTS.md`.

## Kimi Code CLI

En una sesion: `/plugins`, elige Custom, pega
`https://github.com/MKAbuMattar/black-iris`, elige Trust and install. Invoca
con `/skill:black-iris`. Actualizar: `/plugins`, cursor sobre Black Iris,
pulsa `R`. Desinstalar: mismo menu, pulsa `D`.

## Gemini CLI

```bash
gemini extensions install https://github.com/MKAbuMattar/black-iris
```

La extension carga `GEMINI.md`, que importa la habilidad completa, asi que las
reglas aplican desde el primer mensaje. Esta ruta es siempre activa por
construccion. Necesita `git`. Verificar: `gemini extensions list`. Actualizar:
`gemini extensions update black-iris`. Desinstalar:
`gemini extensions uninstall black-iris`.

## OpenCode

OpenCode lee Agent Skills de forma nativa y el modelo las invoca con su
herramienta de habilidades a partir de la descripcion.

```bash
npx skills add MKAbuMattar/black-iris -a opencode -y     # este espacio de trabajo
npx skills add MKAbuMattar/black-iris -a opencode -g -y  # todos los proyectos
```

Manual: copia `skills/black-iris` en `.agents/skills/` del proyecto o en
`~/.config/opencode/skills/`. Pidelo con palabras ("use black-iris"). Sin hook
y sin indicador; pega el fragmento de abajo en `~/.config/opencode/AGENTS.md`.

## Z Code

Z Code lee Agent Skills desde `~/.zcode/skills/<skill-name>/SKILL.md` y deja
que una habilidad referencie otros archivos de su carpeta, asi que las
referencias resuelven.

```bash
mkdir -p ~/.zcode/skills
cp -R skills/black-iris ~/.zcode/skills/
```

O en Z Code: Settings, Skills, Import, y apunta a `skills/black-iris` como
Symlink (sigue este repositorio) o Copy, Global o Project. Pulsa Refresh si una
carpeta copiada a mano no aparece. Invoca con `$black-iris` en el chat o desde
el grupo Skills del menu `/`. Desinstala quitando la carpeta o la importacion.
Sin hook ni indicador; usa el fragmento de abajo en las reglas de Z Code.

## DeepSeek Harness (dsh)

dsh lee Agent Skills como carpetas `<name>/SKILL.md` desde, por prioridad:
`<project>/.dsh/skills`, `<project>/.agents/skills`, cualquier
`customSkillDirs` de la configuracion, `~/.dsh/skills` y `~/.agents/skills`.
La raiz del proyecto es el directorio mas cercano con `.git`. El nombre de la
carpeta debe coincidir con el `name` del frontmatter, y asi es, y las rutas
relativas `references/` resuelven a traves de la carpeta.

```bash
mkdir -p ~/.dsh/skills
cp -R skills/black-iris ~/.dsh/skills/                              # todos los proyectos
mkdir -p .agents/skills && cp -R skills/black-iris .agents/skills/  # solo este proyecto
```

`npx skills add MKAbuMattar/black-iris -a codex` cae en `.agents/skills/`, que
dsh tambien escanea. Copia en lugar de enlazar; seguir enlaces simbolicos es
un ajuste del proveedor que puede estar apagado. dsh respeta las mismas claves
`disable-model-invocation` y `user-invocable` que Claude Code, ambas por
defecto en true, asi que black-iris esta disponible para la herramienta de
habilidades del modelo y para ti por nombre. Sin hook ni indicador; pon el
fragmento de abajo en el system prompt del perfil o en `AGENTS.md`. La ruta de
plugin (`dsh plugin add github:<owner>/<repo>`) necesita un plugin Cordis que
registre un SkillProvider; black-iris no lo incluye, porque la raiz de
habilidades hace el mismo trabajo.

## T3 Code

T3 Code es una interfaz de escritorio que dirige Codex o Claude Code por
debajo. No tiene su propio almacen de habilidades. Instala black-iris en el
agente que T3 Code use, con la ruta de Claude Code o de Codex de arriba, y
luego invocalo en el chat de T3 Code de la misma forma. Con la ruta de plugin
de Claude Code, el hook tambien funciona ahi.

## GitHub Copilot (VS Code y Copilot CLI)

Copilot lee Agent Skills de forma nativa desde `.github/skills/`,
`.claude/skills/` y `.agents/skills/` en el proyecto, y `~/.copilot/skills/`,
`~/.claude/skills/` y `~/.agents/skills/` de forma global.

```bash
npx skills add MKAbuMattar/black-iris -a github-copilot        # este proyecto
npx skills add MKAbuMattar/black-iris -a github-copilot -g     # todos los proyectos
```

Manual: `cp -R skills/black-iris ~/.copilot/skills/`. Escribe `/black-iris`
en el chat. La instalacion solo habilidad de Claude Code tambien sirve para
Copilot, porque escanea `~/.claude/skills/`. Actualizar:
`npx skills update black-iris`. Desinstalar: `npx skills remove black-iris`.
Siempre activo: el fragmento de abajo en `.github/copilot-instructions.md`.

## Zed

El agente de Zed lee Agent Skills. Copia la carpeta completa, porque la
importacion por URL solo toma SKILL.md y black-iris necesita su directorio
`references/`:

```bash
cp -R skills/black-iris ~/.config/zed/skills/
```

Escribe `/black-iris` en el Agent Panel. Verifica en el gestor de Skills.
Desinstalar: borra `~/.config/zed/skills/black-iris`. Siempre activo: el
fragmento de abajo en `~/.config/zed/AGENTS.md`.

## Hermes

```bash
hermes skills install MKAbuMattar/black-iris/skills/black-iris
```

Escribe `/black-iris`. Verificar: `hermes skills list`. Actualizar:
`hermes skills update black-iris`. Desinstalar:
`hermes skills uninstall black-iris`. Siempre activo: el fragmento de abajo en
el `AGENTS.md` del directorio de trabajo, o en tu `SOUL.md` de persona para
todas las sesiones.

## Pi

```bash
pi install https://github.com/MKAbuMattar/black-iris
```

El paquete expone la habilidad; escribe `/skill:black-iris`. Verificar:
`pi list`. Actualizar: `pi update https://github.com/MKAbuMattar/black-iris`.
Desinstalar: `pi remove https://github.com/MKAbuMattar/black-iris`. No se
incluye extension de Pi, asi que no hay conmutador en el pie ni indicador
siempre activo en Pi.

## Antigravity

```bash
agy plugin install https://github.com/MKAbuMattar/black-iris
```

Verificar: `agy plugin list`. Actualizar: desinstala y vuelve a instalar.
Desinstalar: `agy plugin uninstall black-iris`, o `agy plugin disable black-iris`
para conservarlo. Siempre activo: el fragmento de abajo en `~/.gemini/GEMINI.md`.

## Cline

```bash
npx skills add MKAbuMattar/black-iris -a cline        # este proyecto, .agents/skills/
npx skills add MKAbuMattar/black-iris -a cline -g     # todos los proyectos, ~/.agents/skills/
```

Manual: copia `skills/black-iris` en `.agents/skills/` o `~/.agents/skills/`.
Pidelo por nombre en el chat. Siempre activo: el fragmento de abajo en
`.clinerules`.

## TRAE

```bash
npx skills add MKAbuMattar/black-iris -a trae         # este proyecto, .trae/skills/
npx skills add MKAbuMattar/black-iris -a trae -g      # todos los proyectos, ~/.trae/skills/
```

Manual: copia `skills/black-iris` en `.trae/skills/` o `~/.trae/skills/`.
Siempre activo: el fragmento de abajo en las reglas de proyecto de TRAE.

## Qoder

```bash
npx skills add MKAbuMattar/black-iris -a qoder        # este proyecto, .qoder/skills/
npx skills add MKAbuMattar/black-iris -a qoder -g     # todos los proyectos, ~/.qoder/skills/
```

Manual: copia `skills/black-iris` en `.qoder/skills/` o `~/.qoder/skills/`.
Siempre activo: el fragmento de abajo en las reglas de Qoder.

## Droid (Factory)

```bash
npx skills add MKAbuMattar/black-iris -a droid        # este proyecto, .agents/skills/
npx skills add MKAbuMattar/black-iris -a droid -g     # todos los proyectos, ~/.factory/skills/
```

Manual: copia `skills/black-iris` en `.agents/skills/` o `~/.factory/skills/`.
Reinicia `droid` para que vuelva a escanear las habilidades; invoca por si solo
las que coinciden con la descripcion. Siempre activo: el fragmento de abajo en
`AGENTS.md`.

## Kilo Code

```bash
npx skills add MKAbuMattar/black-iris -a kilo         # este proyecto, .agents/skills/
npx skills add MKAbuMattar/black-iris -a kilo -g      # todos los proyectos, ~/.kilo/skills/
```

Manual: copia `skills/black-iris` en `.agents/skills/` o `~/.kilo/skills/`.
Siempre activo: el fragmento de abajo en `.kilocode/rules/`.

## Roo Code

```bash
npx skills add MKAbuMattar/black-iris -a roo          # este proyecto, .roo/skills/
npx skills add MKAbuMattar/black-iris -a roo -g       # todos los proyectos, ~/.roo/skills/
```

Manual: copia `skills/black-iris` en `.roo/skills/` o `~/.roo/skills/`.
Siempre activo: el fragmento de abajo en `.roo/rules/`.

## Crush

```bash
npx skills add MKAbuMattar/black-iris -a crush        # este proyecto, .crush/skills/
npx skills add MKAbuMattar/black-iris -a crush -g     # todos los proyectos, ~/.config/crush/skills/
```

Manual: copia `skills/black-iris` en `.crush/skills/` o
`~/.config/crush/skills/`. Siempre activo: el fragmento de abajo en `CRUSH.md`
o `AGENTS.md`, que Crush lee como contexto.

## Goose

Goose lee `.goose/skills/` y `.agents/skills/` en el proyecto y
`~/.config/goose/skills/` de forma global, y tambien recoge
`~/.claude/skills/`, asi que la instalacion solo habilidad de Claude Code ya lo
cubre. El nombre de la carpeta debe coincidir con el nombre del frontmatter, y
asi es.

```bash
npx skills add MKAbuMattar/black-iris -a goose        # este proyecto, .goose/skills/
npx skills add MKAbuMattar/black-iris -a goose -g     # todos los proyectos, ~/.config/goose/skills/
```

Siempre activo: el fragmento de abajo en `.goosehints`.

## Eigent

Eigent incluye un catalogo de habilidades: `npx @eigent-ai/agent-skills list`
y `npx @eigent-ai/agent-skills install <name>`. Su documentacion no dice donde
quedan en disco ni como anadir una habilidad fuera del catalogo, asi que
todavia no hay una ruta verificada para black-iris. Lo que funciona hoy: pega
el fragmento siempre activo de abajo en el system prompt o en las
instrucciones de tarea del agente, manten `skills/black-iris` en una carpeta
del espacio de trabajo que el agente pueda leer, y pidelo por nombre. Abre un
issue si encuentras la ruta de habilidades personalizadas en los ajustes de
Eigent.

## OpenClaw

OpenClaw tiene un instalador nativo de habilidades y lee carpetas `SKILL.md`
con frontmatter `name` y `description`.

```bash
openclaw skills install MKAbuMattar/black-iris/skills/black-iris            # skills/ del espacio activo
openclaw skills install MKAbuMattar/black-iris/skills/black-iris --global   # ~/.openclaw/skills/
```

Manual: copia `skills/black-iris` en `~/.openclaw/skills/` o en la carpeta
`skills/` del espacio de trabajo. La habilidad toma su nombre del frontmatter,
asi que una subcarpeta vale. Siempre activo: el fragmento de abajo en la
persona del agente o en las instrucciones del espacio de trabajo.

## SillyTavern

SillyTavern es un frontend de chat sin cargador de habilidades. Dos opciones
honestas:

1. Pega el fragmento siempre activo de abajo en el system prompt de tu preset,
   o en la descripcion de una tarjeta de personaje, para que Shape y la Cut
   list apliquen.
2. Para un modo completo, pega el cuerpo de la referencia que necesites (por
   ejemplo `references/deslop.md`) como Author's Note o como entrada de
   lorebook siempre activa, e invocalo por nombre en el chat.

Sin hook, sin almacen, sin comando `/black-iris`.

## Qwen Code

```bash
qwen extensions install MKAbuMattar/black-iris
```

El `qwen-extension.json` incluido apunta Qwen Code a `skills/`. Qwen Code
tambien lee Agent Skills desde `~/.qwen/skills/` y `.qwen/skills/`
directamente, segun su documentacion de habilidades, asi que una copia simple
tambien sirve. Escribe `/black-iris`, o ejecuta `/skills` para confirmar que
aparece. Verificar: `qwen extensions list`. Actualizar:
`qwen extensions update black-iris`. Desinstalar:
`qwen extensions uninstall black-iris`.

## Windsurf

Cascade lee `.windsurf/skills/` en el proyecto y `~/.codeium/windsurf/skills/`
de forma global, segun la documentacion de habilidades de Windsurf.

```bash
npx skills add MKAbuMattar/black-iris -a windsurf        # este proyecto
npx skills add MKAbuMattar/black-iris -a windsurf -g     # todos los proyectos
```

Siempre activo: el fragmento de abajo en una regla de Windsurf con disparador
siempre activo.

## Warp

Los agentes de Warp leen Agent Skills desde `.agents/skills/` en el proyecto
y `~/.agents/skills/` de forma global, segun la documentacion de Warp.

```bash
npx skills add MKAbuMattar/black-iris -a warp            # este proyecto
npx skills add MKAbuMattar/black-iris -a warp -g         # todos los proyectos
```

Siempre activo: el fragmento de abajo en las reglas de agente de Warp.

## Junie (JetBrains)

Junie lee `.junie/skills/` en el proyecto y `~/.junie/skills/` de forma
global, segun su documentacion de agent skills. Copia `skills/black-iris` en
cualquiera de los dos. Siempre activo: el fragmento de abajo en
`.junie/guidelines.md`.

## JetBrains AI Assistant

AI Assistant carga los directorios de habilidades configurados en Settings,
Tools, AI Assistant, Skills, segun su pagina de ayuda de agent skills.
Apuntalo a una copia de `skills/black-iris`. Siempre activo: el fragmento de
abajo en las reglas de proyecto del asistente.

## Mistral Vibe

Vibe sigue la especificacion Agent Skills y lee `~/.vibe/skills/` y
`.vibe/skills/`, segun la documentacion de Mistral Vibe. Copia
`skills/black-iris` en cualquiera de los dos e invoca por nombre.

## OpenHands

OpenHands lee `.agents/skills/` (recomendado) y el antiguo
`.openhands/skills/`, segun su documentacion de habilidades.

```bash
mkdir -p .agents/skills && cp -R skills/black-iris .agents/skills/
```

Siempre activo: el fragmento de abajo en `.openhands/microagents/repo.md`.

## Otros destinos de la CLI de skills

La CLI de skills conoce el directorio de habilidades de muchos mas agentes.
Estas rutas vienen de la tabla de agentes de esa CLI y no se comprobaron
contra la documentacion de cada fabricante; tomalas como punto de partida.

```bash
npx skills add MKAbuMattar/black-iris -a augment       # .augment/skills, ~/.augment/skills
npx skills add MKAbuMattar/black-iris -a continue      # .continue/skills, ~/.continue/skills
npx skills add MKAbuMattar/black-iris -a devin         # .devin/skills, ~/.config/devin/skills (Devin for Terminal)
npx skills add MKAbuMattar/black-iris -a tabnine       # .tabnine/agent/skills
npx skills add MKAbuMattar/black-iris -a kiro          # .kiro/skills; el fragmento del IDE va en .kiro/steering/
npx skills add MKAbuMattar/black-iris -a replit        # .agents/skills
npx skills add MKAbuMattar/black-iris -a grok          # .grok/skills
npx skills add MKAbuMattar/black-iris --all            # todos los agentes que la CLI detecte en esta maquina
```

La misma CLI cubre la cola larga: Lingma, CodeBuddy, CodeArts Agent, Rovo
Dev, Cortex Code, MiniMax Code, iFlow CLI, AiderDesk, Zencoder y otros.
`--all` instala en los que encuentre.

## Agentes sin cargador de habilidades

Aider, Amazon Q Developer, Gemini Code Assist, Sourcegraph Cody, Void, Xcode,
Bolt, v0, Lovable, Manus y Devin en la nube no leen carpetas de habilidades.
Para ellos, pega el fragmento siempre activo de abajo en las instrucciones
persistentes que si lean: reglas de Amazon Q, `GEMINI.md` o `AGENTS.md` para
Gemini Code Assist, un archivo de reglas de proyecto en los demas. Los modos
que necesitan un archivo de referencia no estan disponibles ahi.

## Cursor, Amp y otros harnesses de agent-skills

```bash
npx skills add MKAbuMattar/black-iris                  # este espacio de trabajo
npx skills add MKAbuMattar/black-iris -g               # todos los proyectos
npx skills add MKAbuMattar/black-iris -a cursor -y     # un solo agente
npx skills add MKAbuMattar/black-iris --all            # todos los agentes que detecte la CLI
```

Manual: copia `skills/black-iris` en la ruta que tu agente escanea, por
ejemplo `~/.cursor/skills/`. Copia, no enlaces; Cursor no sigue enlaces
simbolicos en todas las plataformas. Chat nuevo, escribe `/black-iris`.
Verificar: `npx skills list` (`npx skills ls -g` si es global). Actualizar:
`npx skills update black-iris`. Desinstalar: `npx skills remove black-iris`.
Siempre activo: Cursor Settings, Rules, User Rules, o una regla de proyecto
en `.cursor/rules/` con `alwaysApply: true`.

## Cualquier otro agente (manual)

1. Copia `skills/black-iris/` entera, con `references/`, en el directorio que
   tu agente escanea en busca de habilidades. Si no escanea ninguno, ponla en
   cualquier sitio que el agente pueda leer.
2. Si el agente no puede leer frontmatter YAML, dale solo el cuerpo:

   ```bash
   awk '/^---[[:space:]]*$/ && c<2 { c++; next } c>=2' skills/black-iris/SKILL.md
   ```

   Pega eso en el system prompt o en el archivo de reglas, y dile al agente
   donde esta la carpeta `references/` para que las rutas de la tabla
   resuelvan.
3. Invoca por nombre en el primer mensaje de una sesion.

## Fragmento siempre activo para agentes sin hook

Pegalo en el archivo de reglas persistentes del agente. Lleva solo el nucleo
siempre activo; los demas modos siguen necesitando la carpeta de la habilidad
instalada.

```markdown
## black-iris core

Shape every response for a reader with ADHD. Line one is the answer or the
action. Number multi-step work, fewest steps that work. Restate state every
turn. Numbers, thresholds, and scoped conditions stay exact. A warning is the
last thing to cut. An answer stops at its point; a deliverable ships bare.
Estimates in concrete units, saying whose time. Show what now works. Cap lists
at five. End with one action under two minutes, or the blocking question, and
nothing after it.

Build: read the flow the change touches, surface assumptions, every changed
line traces to the request, state the check before the work, minimum code in
the repo's idiom, comments carry the why.

Cut: no em or en dashes, no AI vocabulary (delve, leverage, seamless,
robust, crucial, showcase, utilize), no "not just X but Y", no filler, no
rule of three, name the actor, no decorative emoji or title case, never sign
work as AI. Delete any opener that announces and any closer that recaps.

Break these when asked to explain, before a destructive action, after three
failed fixes, or when a wrong guess costs a rewrite. "stop black-iris" turns
them off.
```

El fragmento se deja en ingles a proposito: es texto de instruccion para el
modelo, y las reglas nombran palabras inglesas concretas.

## Comprobar que funciona

Haz a cualquier agente una pregunta breve de como hacer algo tras invocar la
habilidad. La primera linea debe ser un comando o un veredicto, no debe haber
rayas largas ni una oferta de cierre, y un riesgo debe estar junto al paso que
protege. Si las respuestas siguen abriendo con "Sure" o cerrando con "Let me
know", abre una sesion nueva; las habilidades se indexan al inicio.

## Solucion de problemas

- `/black-iris` no aparece en el autocompletado: reinicia el agente.
- El indicador siempre activo no hace nada: necesita la ruta de plugin de
  Claude Code, no el enlace de la habilidad, y una sesion nueva tras cargar el
  plugin.
- `marketplace add` falla: usa la forma `owner/repo`, o una ruta local a la
  raiz del repositorio, no a `.claude-plugin/`.
- Una ruta de referencia no resuelve: el agente recibio SKILL.md sin su
  carpeta. Reinstala el directorio `skills/black-iris/` completo.
