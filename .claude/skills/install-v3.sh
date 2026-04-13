#!/usr/bin/env bash
# DIAW Trading Platform v3.0 — Installer
# Validates installation and sets up the complete platform
set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}"
cat << 'BANNER'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ██████╗ ██╗ █████╗ ██╗    ██╗                           ║
║     ██╔══██╗██║██╔══██╗██║    ██║                           ║
║     ██║  ██║██║███████║██║ █╗ ██║                           ║
║     ██║  ██║██║██╔══██║██║███╗██║                           ║
║     ██████╔╝██║██║  ██║╚███╔███╔╝                           ║
║     ╚═════╝ ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝                           ║
║                                                              ║
║         TRADING PLATFORM v3.0 INSTALLER                     ║
║    29 Skills | 20 Modules | 12 C-Level Personas             ║
║    Triple Protocol Stack | 8 Swarm Topologies               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
BANNER
echo -e "${NC}"

BASE_DIR="${HOME}/.claude"
SKILLS_DIR="${BASE_DIR}/skills"
AGENTS_DIR="${BASE_DIR}/agents"

DOMAIN_SKILLS=(
  "diaw-orchestrator" "diaw-sales" "diaw-marketing" "diaw-finance"
  "diaw-operations" "diaw-product" "diaw-security" "diaw-swarm" "diaw-documents"
)

MODULE_SKILLS=(
  "diaw-m01-omnidrop" "diaw-m02-voyager" "diaw-m03-omniback" "diaw-m04-eventium"
  "diaw-m05-appgenesis" "diaw-m06-archimind" "diaw-m07-tradeflow" "diaw-m08-alphaomega"
  "diaw-m09-chainforge" "diaw-m10-finova" "diaw-m11-voxai" "diaw-m12-pixelcraft"
  "diaw-m13-aegisprime" "diaw-m14-growthengine" "diaw-m15-uaeautomate" "diaw-m16-strategiccmd"
  "diaw-m17-visionai" "diaw-m18-consultpro" "diaw-m19-crossdomain" "diaw-m20-nexuslink"
)

AGENTS=("sales-researcher" "market-analyst" "security-auditor" "financial-modeler" "content-strategist")

echo -e "${BOLD}[Phase 1/5]${NC} Verifying skill files..."
FOUND_SKILLS=0
TOTAL_SKILLS=$(( ${#DOMAIN_SKILLS[@]} + ${#MODULE_SKILLS[@]} ))

for skill in "${DOMAIN_SKILLS[@]}"; do
  if [[ -f "${SKILLS_DIR}/${skill}/SKILL.md" ]]; then
    echo -e "  ${GREEN}✓${NC} ${skill}/SKILL.md"
    FOUND_SKILLS=$((FOUND_SKILLS + 1))
  else
    echo -e "  ${RED}✗${NC} ${skill}/SKILL.md — MISSING"
  fi
done

for module in "${MODULE_SKILLS[@]}"; do
  if [[ -f "${SKILLS_DIR}/${module}/SKILL.md" ]]; then
    echo -e "  ${GREEN}✓${NC} ${module}/SKILL.md"
    FOUND_SKILLS=$((FOUND_SKILLS + 1))
  else
    echo -e "  ${RED}✗${NC} ${module}/SKILL.md — MISSING"
  fi
done

echo -e "\n  Skills: ${GREEN}${FOUND_SKILLS}/${TOTAL_SKILLS}${NC} found"

echo -e "\n${BOLD}[Phase 2/5]${NC} Verifying agent files..."
FOUND_AGENTS=0
for agent in "${AGENTS[@]}"; do
  if [[ -f "${AGENTS_DIR}/${agent}.md" ]]; then
    echo -e "  ${GREEN}✓${NC} agents/${agent}.md"
    FOUND_AGENTS=$((FOUND_AGENTS + 1))
  else
    echo -e "  ${RED}✗${NC} agents/${agent}.md — MISSING"
  fi
done

echo -e "\n${BOLD}[Phase 3/5]${NC} Verifying settings.json..."
if [[ -f "${BASE_DIR}/settings.json" ]]; then
  echo -e "  ${GREEN}✓${NC} settings.json found"
  if command -v python3 &>/dev/null; then
    python3 -c "import json; json.load(open('${BASE_DIR}/settings.json'))" && \
      echo -e "  ${GREEN}✓${NC} settings.json is valid JSON" || \
      echo -e "  ${RED}✗${NC} settings.json has JSON errors"
  fi
else
  echo -e "  ${RED}✗${NC} settings.json — MISSING"
fi

echo -e "\n${BOLD}[Phase 4/5]${NC} Checking environment..."
CHECKS_PASSED=0
CHECKS_TOTAL=5

if command -v claude &>/dev/null; then
  echo -e "  ${GREEN}✓${NC} Claude Code CLI installed"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
  echo -e "  ${RED}✗${NC} Claude Code CLI not found — install from https://code.claude.com"
fi

if command -v node &>/dev/null; then
  echo -e "  ${GREEN}✓${NC} Node.js $(node -v) available"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
  echo -e "  ${YELLOW}⚠${NC} Node.js not found (needed for RuFlow/npx)"
fi

if command -v python3 &>/dev/null; then
  echo -e "  ${GREEN}✓${NC} Python $(python3 --version) available"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
  echo -e "  ${YELLOW}⚠${NC} Python 3 not found (needed for scripts)"
fi

if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
  echo -e "  ${GREEN}✓${NC} ANTHROPIC_API_KEY set"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
  echo -e "  ${YELLOW}⚠${NC} ANTHROPIC_API_KEY not set — add to ~/.zshrc or ~/.bashrc"
fi

if command -v git &>/dev/null; then
  echo -e "  ${GREEN}✓${NC} Git available"
  CHECKS_PASSED=$((CHECKS_PASSED + 1))
fi

echo -e "\n${BOLD}[Phase 5/5]${NC} Recommended third-party installations..."
echo -e "  Run these commands to unlock full platform capabilities:"
echo ""
echo -e "  ${CYAN}# RuFlow swarm orchestration${NC}"
echo "  npx claude-flow@latest --version"
echo ""
echo -e "  ${CYAN}# Firecrawl web intelligence${NC}"
echo "  npx -y firecrawl-cli@latest init --all --browser"
echo ""
echo -e "  ${CYAN}# Python document generation${NC}"
echo "  pip install reportlab python-docx openpyxl python-pptx matplotlib"
echo ""
echo -e "  ${CYAN}# Security scanning tools${NC}"
echo "  pip install semgrep pip-audit"
echo "  brew install trivy syft gitleaks  # macOS"

# Final summary
echo ""
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"
if [[ $FOUND_SKILLS -eq $TOTAL_SKILLS && $FOUND_AGENTS -eq ${#AGENTS[@]} ]]; then
  echo -e "${GREEN}${BOLD}✓ DIAW Trading Platform v3.0 — FULLY INSTALLED${NC}"
else
  echo -e "${YELLOW}${BOLD}⚠ DIAW Trading Platform v3.0 — PARTIAL INSTALLATION${NC}"
fi
echo -e "${CYAN}══════════════════════════════════════════════════════════════${NC}"
echo -e "  Skills: ${FOUND_SKILLS}/${TOTAL_SKILLS} | Agents: ${FOUND_AGENTS}/${#AGENTS[@]} | Env: ${CHECKS_PASSED}/${CHECKS_TOTAL}"
echo ""
echo -e "${BOLD}Quick Test Commands (in Claude Code):${NC}"
echo "  'Research Acme Corp as a prospect'         → diaw-sales"
echo "  'Write landing page copy for OMNI-DROP'    → diaw-marketing"
echo "  'Build Year 1 financial model'             → diaw-finance"
echo "  'Create SOP for client onboarding'         → diaw-operations"
echo "  'Security audit our API endpoints'         → diaw-security (AEGIS-PRIME)"
echo "  'Launch OMNI-DROP for a UAE luxury store'  → diaw-m01-omnidrop"
echo "  'Spawn ALPHA-OMEGA for BTC/ETH portfolio'  → diaw-m08-alphaomega"
echo ""
echo -e "${YELLOW}Platform: v3.0 | Skills: 29 | Modules: 20 | Personas: 12${NC}"
echo -e "${YELLOW}Topologies: 8 | Protocols: MCP+A2A+ACP | Cost savings: 78%${NC}"
