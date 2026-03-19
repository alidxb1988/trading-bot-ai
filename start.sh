#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Trading Bot AI — Quick-start script
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Colours ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# ── Check Python ──────────────────────────────────────────────────────────────
python3 --version &>/dev/null || error "Python 3 is required"
info "Python: $(python3 --version)"

# ── Virtual environment ───────────────────────────────────────────────────────
if [ ! -d "venv" ]; then
    info "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

# ── Install dependencies ──────────────────────────────────────────────────────
info "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r backend/requirements.txt

# ── .env check ───────────────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
    warn ".env not found — copying .env.example (PAPER MODE)"
    cp .env.example .env
fi

# ── Start server ──────────────────────────────────────────────────────────────
info "Starting Trading Bot AI on http://0.0.0.0:8000"
info "Open your browser → http://localhost:8000"
echo ""

exec python3 -m uvicorn backend.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info
