#!/bin/bash
# Automated Skill Security Scanner v2
# Part of skill-vetter - Security-first skill vetting for AI agents

set -euo pipefail

SKILL_DIR="${1:-.}"

echo "=========================================="
echo "SKILL VETTER - Automated Security Scan v2"
echo "=========================================="
echo "Scanning: $SKILL_DIR"
echo ""

RED_FLAGS=0
WARNINGS=0

CURL_PATTERNS=("curl " "curl -" "wget " "wget -" "fetch(" "http.request" "https.request" "exec\s*(" "child_process")
EXEC_PATTERNS=("exec(" "eval(" "spawn(" "child_process" "system(")
CRED_PATTERNS=("~/.ssh" "~/.aws" "~/.config" ".pem" ".key" "id_rsa" "id_ed25519" "api_key" "API_KEY" "SECRET" "TOKEN" "credential")
DANGEROUS_PATTERNS=("base64" "decode" "obfuscate" "eval(")

echo "=== Pattern Detection ==="

scan_file() {
    local file="$1"
    local relpath="${file#$SKILL_DIR/}"
    
    # Skip non-code files
    [[ "$file" =~ \.(png|jpg|gif|ico|woff|ttf|eot|mp3|mp4|pdf|md)$ ]] && return 0
    [[ "$file" =~ \.git|\.lock$|node_modules ]] && return 0
    
    while IFS= read -r line; do
        linenum=$(echo "$line" | cut -d: -f1)
        content=$(echo "$line" | cut -d: -f2-)
        
        # Skip comment-only lines
        [[ "$content" =~ ^[[:space:]]*// ]] && continue
        [[ "$content" =~ ^[[:space:]]*# ]] && [[ ! "$content" =~ \$\( ]] && continue
        
        for pattern in "${CURL_PATTERNS[@]}"; do
            if [[ "$content" == *"$pattern"* ]]; then
                echo "🚨 CURL/WGET: $relpath:$linenum"
                ((RED_FLAGS++))
            fi
        done
        
        for pattern in "${EXEC_PATTERNS[@]}"; do
            if [[ "$content" == *"$pattern"* ]]; then
                echo "🚨 EXEC: $relpath:$linenum - $pattern"
                ((RED_FLAGS++))
            fi
        done
        
        for pattern in "${CRED_PATTERNS[@]}"; do
            if [[ "$content" == *"$pattern"* ]]; then
                echo "🚨 CRED: $relpath:$linenum - $pattern"
                ((RED_FLAGS++))
            fi
        done
        
        for pattern in "${DANGEROUS_PATTERNS[@]}"; do
            if [[ "$content" == *"$pattern"* ]]; then
                echo "⚠️  DANGER: $relpath:$linenum - suspicious: $pattern"
                ((WARNINGS++))
            fi
        done
    done < <(grep -rn "" "$file" 2>/dev/null || true)
}

# Scan src/ directory
if [[ -d "$SKILL_DIR/src" ]]; then
    echo "Scanning: src/"
    find "$SKILL_DIR/src" -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.sh" \) 2>/dev/null | while read -r f; do
        scan_file "$f"
    done
fi

# Scan index files
for f in "$SKILL_DIR/index.ts" "$SKILL_DIR/index.js" "$SKILL_DIR/index.py"; do
    [[ -f "$f" ]] && scan_file "$f"
done

echo ""
echo "=========================================="
echo "SCAN SUMMARY"
echo "=========================================="
echo "Red Flags (🚨): $RED_FLAGS"
echo "Warnings (⚠️):  $WARNINGS"
echo ""

[[ $RED_FLAGS -gt 0 ]] && echo "VERDICT: ❌ DO NOT INSTALL" && exit 1
[[ $WARNINGS -gt 0 ]] && echo "VERDICT: ⚠️ INSTALL WITH CAUTION" && exit 0
echo "VERDICT: ✅ LIKELY SAFE"
exit 0
