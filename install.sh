#!/bin/bash
# ----------------------------------------------------------
# httpulse - Installer Script
# Author : Saqib Siddique (@saqibsec)
# GitHub : https://github.com/saqibsec/httpulse
# ----------------------------------------------------------

GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  Installing httpulse..."
echo "  Author : Saqib Siddique (@saqibsec)"
echo "  GitHub : https://github.com/saqibsec/httpulse"
echo -e "${NC}"

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] python3 not found. Please install Python 3 first.${NC}"
    exit 1
fi

# Check pip3
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}[ERROR] pip3 not found. Run: sudo apt install python3-pip${NC}"
    exit 1
fi

# Install dependencies
echo -e "${CYAN}[*] Installing dependencies...${NC}"
pip3 install -r requirements.txt --break-system-packages --quiet

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to install dependencies.${NC}"
    exit 1
fi

# Copy to /usr/local/bin
echo -e "${CYAN}[*] Copying httpulse to /usr/local/bin/...${NC}"
sudo cp httpulse.py /usr/local/bin/httpulse
sudo chmod +x /usr/local/bin/httpulse

if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to install. Try running with sudo.${NC}"
    exit 1
fi

echo -e "${GREEN}"
echo "  [+] httpulse installed successfully!"
echo "  [+] Run it from anywhere: httpulse -h"
echo -e "${NC}"
