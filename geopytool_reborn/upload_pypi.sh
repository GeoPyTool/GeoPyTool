#!/usr/bin/env bash
# GeoPyTool Reborn - Build and upload to PyPI
set -e
cd "$(dirname "${BASH_SOURCE[0]}")"

PYTHON="${PYTHON:-python3}"
VERSION_FILE="src/geopytool_reborn/__init__.py"

echo "=== GeoPyTool Reborn PyPI Upload ==="

echo "[1/5] Bumping patch version..."
"$PYTHON" -c "
import re, sys
p = '$VERSION_FILE'
t = open(p, encoding='utf-8').read()
m = re.search(r'(__version__\s*=\s*\"(\d+\.\d+\.)(\d+)\")', t)
if not m: print('ERROR: cannot parse version'); sys.exit(1)
old_v = m.group(2) + m.group(3)
new_v = m.group(2) + str(int(m.group(3)) + 1)
open(p, 'w', encoding='utf-8').write(t.replace(m.group(1), '__version__ = \"' + new_v + '\"'))
print(f'  {old_v} -> {new_v}')
"

echo "[2/5] Cleaning old builds..."
rm -rf dist/ build/ *.egg-info src/geopytool_reborn.egg-info

echo "[3/5] Installing build tools..."
"$PYTHON" -m pip install --upgrade build twine -q

echo "[4/5] Building package..."
"$PYTHON" -m build
"$PYTHON" -m twine check dist/*

echo "[5/5] Uploading to PyPI..."
"$PYTHON" -m twine upload dist/*

echo "=== Done! ==="