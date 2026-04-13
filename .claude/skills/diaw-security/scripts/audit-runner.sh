#!/usr/bin/env bash
# DIAW Trading — Security Audit Runner
# Runs automated security checks on the codebase
# Usage: ./audit-runner.sh [--target ./src] [--output ./security-report]
set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

TARGET="${1:-./src}"
OUTPUT_DIR="${2:-./security-report-$(date +%Y%m%d)}"
ISSUES=0

mkdir -p "$OUTPUT_DIR"

echo -e "${CYAN}${BOLD}DIAW AEGIS-PRIME — Security Audit Runner${NC}"
echo -e "${CYAN}Target: ${TARGET} | Output: ${OUTPUT_DIR}${NC}"
echo "============================================"

# Function to run a check
run_check() {
    local name="$1"
    local cmd="$2"
    local output_file="$3"
    echo -ne "  ${YELLOW}[RUNNING]${NC} ${name}..."
    if eval "$cmd" > "$OUTPUT_DIR/$output_file" 2>&1; then
        echo -e "\r  ${GREEN}[PASS]${NC}    ${name}"
    else
        echo -e "\r  ${RED}[ISSUES]${NC}  ${name} — see ${output_file}"
        ISSUES=$((ISSUES + 1))
    fi
}

echo -e "\n${BOLD}[1/6] Dependency Audit${NC}"
if command -v npm &>/dev/null; then
    run_check "NPM Audit" "npm audit --audit-level=moderate --json" "npm-audit.json"
fi
if command -v pip &>/dev/null; then
    run_check "Python Pip-Audit" "pip-audit -r requirements.txt --format json" "pip-audit.json" || true
fi

echo -e "\n${BOLD}[2/6] Static Analysis (Semgrep)${NC}"
if command -v semgrep &>/dev/null; then
    run_check "OWASP Top 10" "semgrep --config=p/owasp-top-ten ${TARGET} --json" "semgrep-owasp.json"
    run_check "Secrets Detection" "semgrep --config=p/secrets ${TARGET} --json" "semgrep-secrets.json"
    run_check "JavaScript Security" "semgrep --config=p/javascript ${TARGET} --json" "semgrep-js.json"
else
    echo -e "  ${YELLOW}[SKIP]${NC} Semgrep not installed. Run: pip install semgrep"
fi

echo -e "\n${BOLD}[3/6] Container Security${NC}"
if command -v trivy &>/dev/null; then
    run_check "Trivy FS Scan (CRITICAL/HIGH)" \
        "trivy fs --severity HIGH,CRITICAL --format json ${TARGET}" \
        "trivy-fs.json"
    if [ -f "Dockerfile" ]; then
        run_check "Trivy Image Scan" \
            "trivy image --format json $(basename $(pwd)):latest" \
            "trivy-image.json"
    fi
else
    echo -e "  ${YELLOW}[SKIP]${NC} Trivy not installed. Run: brew install trivy"
fi

echo -e "\n${BOLD}[4/6] Secrets Detection${NC}"
if command -v trufflehog &>/dev/null; then
    run_check "TruffleHog Secrets Scan" \
        "trufflehog filesystem ${TARGET} --json" \
        "trufflehog.json"
elif command -v gitleaks &>/dev/null; then
    run_check "Gitleaks Secrets Scan" \
        "gitleaks detect --source ${TARGET} --report-format json --report-path ${OUTPUT_DIR}/gitleaks.json" \
        "gitleaks.json"
else
    echo -e "  ${YELLOW}[SKIP]${NC} No secrets scanner installed. Run: brew install gitleaks"
fi

echo -e "\n${BOLD}[5/6] Security Headers Check${NC}"
if command -v curl &>/dev/null; then
    HEADERS_FILE="$OUTPUT_DIR/security-headers.txt"
    if [ -n "${APP_URL:-}" ]; then
        echo "Checking: $APP_URL"
        curl -sI "$APP_URL" | grep -iE "(strict-transport|content-security|x-frame|x-content-type|referrer-policy)" > "$HEADERS_FILE" || true
        echo -e "  ${GREEN}[DONE]${NC}   Security headers — see security-headers.txt"
    else
        echo -e "  ${YELLOW}[SKIP]${NC} Set APP_URL environment variable to check headers"
    fi
fi

echo -e "\n${BOLD}[6/6] SBOM Generation${NC}"
if command -v syft &>/dev/null; then
    run_check "Generate SBOM (CycloneDX)" \
        "syft ${TARGET} -o cyclonedx-json" \
        "sbom.json"
else
    echo -e "  ${YELLOW}[SKIP]${NC} Syft not installed. Run: brew install syft"
fi

# Summary report
echo ""
echo "============================================"
REPORT="$OUTPUT_DIR/summary.md"
{
    echo "# DIAW Security Audit Report"
    echo "Date: $(date)"
    echo "Target: $TARGET"
    echo ""
    echo "## Summary"
    echo "- Issues flagged: $ISSUES categories"
    echo ""
    echo "## Files Generated"
    ls "$OUTPUT_DIR/"
    echo ""
    echo "## Next Steps"
    echo "1. Review each output file for specific findings"
    echo "2. Prioritize Critical > High > Medium > Low"
    echo "3. Create tickets for each issue with remediation"
    echo "4. Re-run after fixes to verify remediation"
} > "$REPORT"

if [ "$ISSUES" -eq 0 ]; then
    echo -e "${GREEN}${BOLD}✓ All checks passed! Report: ${OUTPUT_DIR}/summary.md${NC}"
else
    echo -e "${YELLOW}${BOLD}⚠ ${ISSUES} check(s) found issues. Review: ${OUTPUT_DIR}/summary.md${NC}"
fi
