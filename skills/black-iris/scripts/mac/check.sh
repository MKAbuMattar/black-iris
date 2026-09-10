#!/usr/bin/env bash
# macOS entry point. The bash lint uses only BSD-safe tools and bash 3.2
# features, so one copy lives in linux/ and this delegates to it.
exec bash "$(dirname "$0")/../linux/check.sh" "$@"
