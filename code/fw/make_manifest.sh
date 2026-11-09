#!/usr/bin/env bash
# Extends data/MANIFEST.sha256: v0.1 entries first (unchanged files, verified), then every v0.2 data file
# (fw_*; logs and data/cache/ excluded, as in v0.1).
set -euo pipefail
cd "$(dirname "$0")/../../data"
head -10 MANIFEST.sha256 > MANIFEST.v01.tmp
shasum -a 256 -c MANIFEST.v01.tmp > /dev/null
{ cat MANIFEST.v01.tmp; find . -path ./cache -prune -o -type f -path './fw_*' -print | sed 's|^\./||' | LC_ALL=C sort | xargs shasum -a 256; } > MANIFEST.sha256.new
mv MANIFEST.sha256.new MANIFEST.sha256
mv MANIFEST.v01.tmp cache/MANIFEST.v01.check
echo "manifest: $(wc -l < MANIFEST.sha256 | tr -d ' ') files"
