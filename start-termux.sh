#!/data/data/com.termux/files/usr/bin/sh
set -eu
cd "$(dirname "$0")"
command -v python >/dev/null 2>&1 || { echo "Install Python first: pkg install python"; exit 1; }
exec python serve.py
