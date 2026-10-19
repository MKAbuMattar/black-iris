# Shared by the hooks. Sourced, never run on its own. POSIX sh.

# The store slug, the same rule as references/memory.md: the project path
# with / as -. A Windows path becomes /c/... first, so C:\x, C:/x, and /c/x
# share one store whichever shell handed the path over.
slug() {
  p=$(printf '%s' "$1" | tr '\\' '/')
  case "$p" in [A-Za-z]:/*) p="/$(printf '%s' "${p%%:*}" | tr 'A-Z' 'a-z')${p#?:}" ;; esac
  printf '%s' "$p" | tr '/' '-'
}

# A Python that runs. On Windows, python3 can be the Store stub: the command
# exists and exits 49, so finding it on PATH proves nothing.
find_python() {
  for c in python3 python py; do
    "$c" -c 1 >/dev/null 2>&1 && { printf '%s' "$c"; return 0; }
  done
  return 1
}
