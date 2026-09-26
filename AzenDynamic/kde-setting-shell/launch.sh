#!/usr/bin/env bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# 直接用虚拟环境里的 python 绝对路径
PY="/home/admin/myenv/bin/python3"

# 记录启动日志，方便排查
LOG="$PROJECT_DIR/launch.log"
exec > "$LOG" 2>&1

echo "=== $(date) ==="
echo "PY=$PY"
echo "PATH=$PATH"

if [ ! -x "$PY" ]; then
    echo "ERROR: $PY not found or not executable"
    exit 1
fi

echo "Starting main.py..."
exec "$PY" "$PROJECT_DIR/main.py" "$@"