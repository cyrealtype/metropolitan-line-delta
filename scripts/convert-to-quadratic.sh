#!/bin/bash

# convert-to-quadratic.sh - Convert all UFOs in /sources folder to quadratic (in-place)
# Usage: From project root: ./scripts/convert-to-quadratic.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Quadratic UFO Converter (In-Place)${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${RED}WARNING: This will modify your original UFO files in-place!${NC}"
echo -e "${YELLOW}A backup will be created before conversion.${NC}"
echo ""

# Check if we're in the project root
if [ ! -d "sources" ]; then
    echo -e "${RED}Error: This script must be run from the project root.${NC}"
    echo -e "Usage: ${GREEN}./scripts/convert-to-quadratic.sh${NC}"
    exit 1
fi

# Check if fonttools is installed
if ! command -v fonttools &> /dev/null; then
    echo -e "${RED}Error: fonttools is not installed.${NC}"
    echo "Install it with: pip install fonttools cu2qu"
    exit 1
fi

# Check if cu2qu is available
if ! fonttools cu2qu --help &> /dev/null; then
    echo -e "${RED}Error: cu2qu not available in fonttools${NC}"
    echo "Install with: pip install cu2qu"
    exit 1
fi

# Go to sources directory
cd sources

# Find only UFO files directly in sources/ (not in subfolders)
UFO_FILES=$(find . -maxdepth 1 -type d -name "*.ufo" 2>/dev/null)

if [ -z "$UFO_FILES" ]; then
    echo -e "${RED}No UFO files found in sources/ folder${NC}"
    cd ..
    exit 1
fi

# Count UFO files
UFO_COUNT=$(echo "$UFO_FILES" | wc -l | tr -d ' ')
echo -e "Found ${GREEN}$UFO_COUNT${NC} UFO file(s) in sources/"
echo ""

# List files to be converted
echo -e "${BLUE}Files to convert:${NC}"
for UFO in $UFO_FILES; do
    echo -e "  • ${YELLOW}$(basename "$UFO")${NC}"
done
echo ""

# Ask for confirmation
read -p "Continue with in-place conversion? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Conversion cancelled.${NC}"
    cd ..
    exit 0
fi

# Create backup
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
echo -e "\n${BLUE}Creating backup in: ${YELLOW}$BACKUP_DIR/${NC}"
mkdir -p "$BACKUP_DIR"
cp -r $UFO_FILES "$BACKUP_DIR/"
echo ""

# Error tolerance (default: 1)
ERROR_TOLERANCE="${1:-1}"

# Process each UFO (in-place)
PROCESSED=0
FAILED=0
FAILED_FILES=()

for UFO in $UFO_FILES; do
    UFO_NAME=$(basename "$UFO")
    
    echo -e "${GREEN}[$((PROCESSED + FAILED + 1))/$UFO_COUNT]${NC} Converting: ${YELLOW}$UFO_NAME${NC}"
    
    # Convert in-place
    if fonttools cu2qu -e "$ERROR_TOLERANCE" "$UFO_NAME" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Successfully converted to quadratic"
        PROCESSED=$((PROCESSED + 1))
    else
        echo -e "  ${RED}✗${NC} Failed to convert"
        FAILED=$((FAILED + 1))
        FAILED_FILES+=("$UFO_NAME")
        
        # Restore from backup
        echo -e "  ${YELLOW}↻${NC} Restoring from backup..."
        rm -rf "$UFO_NAME"
        cp -r "$BACKUP_DIR/$UFO_NAME" "./"
        echo -e "  ${GREEN}✓${NC} Restored original"
    fi
    
    echo ""
done

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Conversion Complete${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Total UFO files: ${YELLOW}$UFO_COUNT${NC}"
echo -e "Successfully converted: ${GREEN}$PROCESSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"

if [ $FAILED -gt 0 ]; then
    echo -e "\n${RED}Failed files (restored from backup):${NC}"
    for file in "${FAILED_FILES[@]}"; do
        echo -e "  • ${YELLOW}$file${NC}"
    done
    echo -e "\n${YELLOW}These files need manual inspection.${NC}"
fi

echo -e "\nBackup stored in: ${YELLOW}$BACKUP_DIR/${NC}"
echo -e "Converted files are now in: ${YELLOW}sources/${NC}"

cd ..

exit 0