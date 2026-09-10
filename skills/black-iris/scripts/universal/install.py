#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""Install black-iris as a personal skill on any OS.

  python3 scripts/universal/install.py               link into ~/.claude/skills
  python3 scripts/universal/install.py --always-on   also inject at every session start
  python3 scripts/universal/install.py --uninstall   remove link and flag

Symlinks on POSIX. On Windows a symlink needs Developer Mode or admin, so it
falls back to a directory copy and says so. The always-on flag only has
effect when the plugin's SessionStart hook is loaded (plugin install), not
for a bare skill link; the flag is still set here so both paths agree.
"""
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2]
HOME = Path.home()
DEST = HOME / ".claude" / "skills" / SKILL.name
FLAG = HOME / ".BLACK_IRIS_AGENTS" / "always-on"


def remove(path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def main(argv):
    if "--uninstall" in argv:
        remove(DEST)
        FLAG.unlink(missing_ok=True)
        print(f"removed {DEST} and {FLAG.name}")
        return 0
    DEST.parent.mkdir(parents=True, exist_ok=True)
    remove(DEST)
    try:
        DEST.symlink_to(SKILL, target_is_directory=True)
        print(f"linked {DEST} -> {SKILL}")
    except OSError as e:
        shutil.copytree(SKILL, DEST)
        print(f"copied {SKILL} -> {DEST} (symlink failed: {e}). Re-run after editing the skill.")
    if "--always-on" in argv:
        FLAG.parent.mkdir(parents=True, exist_ok=True)
        FLAG.touch()
        print(f"always-on flag set: {FLAG}")
    print("Start a new session; skills and hooks load at session start.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
