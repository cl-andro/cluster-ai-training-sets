#!/usr/bin/env bash
set -euo pipefail

# Visual colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}[1/4] Updating packages and installing dependencies...${NC}"
sudo apt update -qq && sudo apt install -y -qq curl ca-certificates

echo -e "${BLUE}[2/4] Checking Ollama installation...${NC}"
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo -e "${GREEN}✓ Ollama is already installed.${NC}"
fi

# Ensure Ollama daemon is running
if command -v systemctl &> /dev/null; then
    sudo systemctl start ollama || true
fi

echo -e "${BLUE}[3/4] Waiting for Ollama background service...${NC}"
RETRIES=0
until curl -s http://localhost:11434/ &> /dev/null || [ $RETRIES -eq 15 ]; do
    sleep 1
    RETRIES=$((RETRIES + 1))
done

if [ $RETRIES -eq 15 ]; then
    echo -e "${RED}Error: Ollama service failed to start.${NC}"
    exit 1
fi

echo -e "${BLUE}[4/4] Fetching GGUF weights and building local 'worker' model...${NC}"

# Create a temporary Modelfile that auto-deletes when script exits
TMP_MODELFILE=$(mktemp)
trap 'rm -f "$TMP_MODELFILE"' EXIT

cat << 'EOF' > "$TMP_MODELFILE"
FROM hf.co/zk-mohammad/cluster-worker-v2-0.5b-GGUF

TEMPLATE """<|im_start|>system
You are a strict, zero-fluff Linux terminal worker. Return strictly the bash command, no explanations, no markdown chat, no formatting.<|im_end|>
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""

PARAMETER temperature 0.0
PARAMETER top_k 1
PARAMETER stop "<|im_end|>"
PARAMETER stop "<|im_start|>"
EOF

# Create the model inside Ollama
ollama create worker -f "$TMP_MODELFILE"

echo ""
echo -e "${GREEN}========================================================${NC}"
echo -e "${GREEN}  SUCCESS! Your 0.5B Worker Model is installed.        ${NC}"
echo -e "${GREEN}========================================================${NC}"
echo -e "Run it anytime using:"
echo -e "  ${BLUE}ollama run worker \"List all hidden files with human-readable sizes.\"${NC}\n"