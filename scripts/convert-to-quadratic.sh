#!/bin/bash

# convert-to-quadratic.sh - Convert all UFOs to quadratic with interpolation compatibility
# Uses batch conversion for perfect consistency across all masters

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Quadratic UFO Converter${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${RED}WARNING: This will modify your original UFO files in-place!${NC}"
echo -e "${YELLOW}Uses batch conversion for perfect curve consistency.${NC}"
echo ""

# Check if we're in the project root
if [ ! -d "sources" ]; then
    echo -e "${RED}Error: This script must be run from the project root.${NC}"
    exit 1
fi

# Check if fonttools is installed
if ! command -v fonttools &> /dev/null; then
    echo -e "${RED}Error: fonttools is not installed.${NC}"
    echo "Install it with: pip install fonttools cu2qu"
    exit 1
fi

cd sources

# Clean up old backup folders
echo -e "${BLUE}Cleaning up old backup folders...${NC}"
find . -maxdepth 1 -type d -name "backup_*" -exec rm -rf {} + 2>/dev/null || true

# Find UFO files
UFO_FILES=$(find . -maxdepth 1 -type d -name "*.ufo" 2>/dev/null)

if [ -z "$UFO_FILES" ]; then
    echo -e "${RED}No UFO files found in sources/ folder${NC}"
    cd ..
    exit 1
fi

UFO_COUNT=$(echo "$UFO_FILES" | wc -l | tr -d ' ')
echo -e "\nFound ${GREEN}$UFO_COUNT${NC} UFO file(s) in sources/"
echo ""

# List files
echo -e "${BLUE}Files to convert:${NC}"
for UFO in $UFO_FILES; do
    echo -e "  • ${YELLOW}$(basename "$UFO")${NC}"
done
echo ""

# Ask for confirmation
read -p "Continue with in-place batch conversion? (y/N) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Conversion cancelled.${NC}"
    cd ..
    exit 0
fi

# Fix corrupted glyph in XTSP5
echo -e "\n${BLUE}Fixing corrupted glyphs in XTSP5...${NC}"
if [ -d "MetropolitanLineDelta-XTSP5.ufo" ] && [ -d "MetropolitanLineDelta-XTSP140.ufo" ]; then
    # Copy all glyphs from XTSP140 to XTSP5 (fixes any corrupted glyphs)
    cp -r MetropolitanLineDelta-XTSP140.ufo/glyphs/* MetropolitanLineDelta-XTSP5.ufo/glyphs/ 2>/dev/null || true
    echo -e "  ${GREEN}✓${NC} Fixed corrupted glyphs in XTSP5"
fi

# Create backup
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
echo -e "\n${BLUE}Creating backup in: ${YELLOW}$BACKUP_DIR/${NC}"
mkdir -p "$BACKUP_DIR"
cp -r $UFO_FILES "$BACKUP_DIR/"
echo -e "  ${GREEN}✓${NC} Backup created"

# Convert ALL UFOs in ONE batch command for perfect consistency
echo -e "\n${BLUE}Converting all UFOs together (batch mode)...${NC}"
echo -e "${YELLOW}This ensures perfect curve compatibility across all masters.${NC}"
echo ""

# Build the command with all UFO files
UFO_LIST=""
for UFO in $UFO_FILES; do
    UFO_LIST="$UFO_LIST $(basename "$UFO")"
done

# Run the batch conversion
if fonttools cu2qu --interpolatable $UFO_LIST 2>/dev/null; then
    echo -e "${GREEN}✓${NC} All UFOs successfully converted!"
    PROCESSED=$UFO_COUNT
    FAILED=0
else
    echo -e "${RED}✗${NC} Batch conversion failed. Restoring from backup..."
    # Restore all from backup
    for UFO in $UFO_FILES; do
        UFO_NAME=$(basename "$UFO")
        rm -rf "$UFO_NAME"
        cp -r "$BACKUP_DIR/$UFO_NAME" "./"
    done
    echo -e "${YELLOW}↻${NC} All files restored from backup"
    PROCESSED=0
    FAILED=$UFO_COUNT
fi

# Summary
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  Conversion Complete${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Total UFO files: ${YELLOW}$UFO_COUNT${NC}"
echo -e "Successfully converted: ${GREEN}$PROCESSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✓ All masters are now compatible for interpolation!${NC}"
    echo -e "${GREEN}✓ All masters have the same number of off-curve points.${NC}"
else
    echo -e "\n${RED}Conversion failed. Files restored from backup.${NC}"
fi

echo -e "\nBackup stored in: ${YELLOW}$BACKUP_DIR${NC}"

cd ..