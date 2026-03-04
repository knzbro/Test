#!/bin/bash
# =============================================
# FB MASS REPORTING TOOL - ALL IN ONE FILE
# Version: 3.0 (Termux Optimized)
# Author: Student Project
# Daily Limit: 100 Reports
# =============================================

# =============================================
# COLOR CODES
# =============================================
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'
BOLD='\033[1m'

# =============================================
# CONFIGURATION VARIABLES
# =============================================
VERSION="3.0"
DAILY_LIMIT=100
DELAY=8
MAX_RETRIES=3
REPORT_COUNT=0
TODAY_REPORTS=0
SCRIPT_NAME=$(basename "$0")
SCRIPT_DIR="$HOME/.fb-tool"
CONFIG_FILE="$SCRIPT_DIR/config.cfg"
ACCOUNTS_FILE="$SCRIPT_DIR/accounts.lst"
PROXIES_FILE="$SCRIPT_DIR/proxies.lst"
LOG_DIR
