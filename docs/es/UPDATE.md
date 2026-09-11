# Actualizar black-iris

Todas las rutas de abajo terminan en lo mismo: la carpeta
`skills/black-iris/` mas reciente en el lugar que tu agente escanea. Busca tu
ruta, ejecuta su comando, abre una sesion nueva. Las habilidades y los hooks se
leen al iniciar la sesion, asi que nada de lo que actualices tiene efecto en la
sesion en la que estas ahora.

Las rutas de instalacion estan en [INSTALL.md](INSTALL.md). Este archivo
solo cubre actualizar algo que ya esta instalado.

## Claude Code

Dos comandos, en este orden.

```bash
claude plugin marketplace update black-iris
claude plugin update black-iris
```

Despues reinicia Claude Code. La CLI dice `restart required to apply`, y lo
dice en serio.

**`add` e `install` no te actualizan.** Ambos son operaciones de creacion.
Sobre una instalacion existente imprimen `already on disk` y `already
installed`, no descargan nada y te dejan en la version vieja. Esta es la forma
mas comun de creer que actualizaste sin haberlo hecho.

Si instalaste solo la habilidad, sin el plugin, vuelve a ejecutar el
instalador, que reemplaza el enlace o la copia en su sitio:

```bash
python3 skills/black-iris/scripts/universal/install.py
```

## Que ruta usaste

| Tu instalacion uso | Actualiza con |
|---|---|
| `claude plugin install` | los dos comandos de arriba, y reinicia |
| `npx skills add` | `npx skills update black-iris` |
| `codex plugin add` | `codex plugin marketplace upgrade black-iris`, luego quitar y volver a agregar |
| `gemini extensions install` | `gemini extensions update black-iris` |
| `qwen extensions install` | `qwen extensions update black-iris` |
| `hermes skills install` | `hermes skills update black-iris` |
| `pi install` | `pi update https://github.com/MKAbuMattar/black-iris` |
| `agy plugin install` | `agy plugin uninstall black-iris`, luego instalar otra vez |
| `openclaw skills install` | ejecuta el comando de instalacion otra vez |
| El menu `/plugins` de Kimi | `/plugins`, mueve el cursor a Black Iris, pulsa `R` |
| `cp -R` a mano | `git pull`, y repite el mismo `cp -R` |
| Solo el fragmento siempre activo | vuelve a pegar el fragmento de `INSTALL.md` |

## La CLI de skills

Un solo comando cubre todos los agentes instalados asi: OpenCode, GitHub
Copilot en VS Code y en la CLI, Kiro, Cline, TRAE, Qoder, Droid, Kilo Code, Roo
Code, Crush, Goose, Windsurf, Warp, Cursor, Amp, la ruta de solo habilidad de
Codex, y la cola larga de "Other skills-CLI targets".

```bash
npx skills update black-iris
npx skills ls          # o: npx skills ls -g   para una instalacion global
```

Si lo instalaste en mas de un agente, la CLI actualiza cada copia que coloco.
Ejecuta `npx skills ls` antes si quieres verlas.

## Gestores por agente

```bash
gemini extensions update black-iris      # Gemini CLI
qwen extensions update black-iris        # Qwen Code
hermes skills update black-iris          # Hermes
pi update https://github.com/MKAbuMattar/black-iris   # Pi
```

Codex y Antigravity no actualizan en el sitio. Codex refresca primero el
marketplace y luego pide quitar y volver a agregar el plugin:

```bash
codex plugin marketplace upgrade black-iris
codex plugin remove black-iris && codex plugin add black-iris@black-iris

agy plugin uninstall black-iris
agy plugin install https://github.com/MKAbuMattar/black-iris
```

Kimi Code CLI se maneja por menu. En una sesion escribe `/plugins`, mueve el
cursor a Black Iris y pulsa `R`.

## Rutas de copia

Z Code, DeepSeek Harness, Oh My Pi, Zed, OpenHands, y cualquier instalacion que
hiciste a mano. Actualiza el repo y repite la copia que usaste, que sobrescribe
en su sitio.

```bash
git pull
cp -R skills/black-iris ~/.zcode/skills/          # Z Code
cp -R skills/black-iris ~/.dsh/skills/            # DeepSeek Harness
cp -R skills/black-iris .agents/skills/           # Oh My Pi
cp -R skills/black-iris ~/.config/zed/skills/     # Zed
```

Copia siempre la carpeta entera. Las referencias viven junto a `SKILL.md`, y
una copia que se lleva solo `SKILL.md` deja ocho modos apuntando a archivos que
no estan.

## Rutas de solo fragmento

GitHub Copilot en JetBrains, Junie, JetBrains AI Assistant, Mistral Vibe,
Eigent, SillyTavern y todos los agentes de "Agents with no skill loader" llevan
el fragmento siempre activo en vez de la carpeta de la habilidad. No hay nada
que actualizar salvo que el fragmento haya cambiado. Compara la seccion
`black-iris core` de `INSTALL.md` con lo que pegaste y reemplazalo si
difieren.

T3 Code funciona sobre Codex o Claude Code. Actualiza el que tenga configurado
y T3 Code lo sigue.

## Funciono?

```bash
claude plugin list          # Claude Code: Version, y Status enabled
npx skills ls               # rutas de la CLI de skills
gemini extensions list      # Gemini CLI
qwen extensions list        # Qwen Code
hermes skills list          # Hermes
```

La version en `.claude-plugin/plugin.json` en `main` es la mas reciente
publicada. Las versiones estan en
<https://github.com/MKAbuMattar/black-iris/releases>.

Luego hazle al agente una pregunta corta de como se hace algo, en una sesion
nueva. La primera linea debe ser un comando o un veredicto, sin ofrecimiento
final.

## Cuando la actualizacion no cambia nada

1. **No reiniciaste.** Las habilidades y los hooks se indexan al iniciar la
   sesion.
2. **Volviste a ejecutar `add` o `install`.** No hacen nada sobre una
   instalacion existente. Usa el comando `update` de tu ruta.
3. **Tienes dos copias.** Una instalacion global y una de proyecto de la misma
   habilidad se resuelven las dos; actualiza ambas o elimina la que no quieras.
4. **`Status: failed to load` en el plugin de Claude Code.** Fue un error del
   manifiesto en todas las versiones hasta la 1.6.0. La correccion solo llega
   actualizando, asi que ejecuta los dos comandos de arriba y reinicia.
