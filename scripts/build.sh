#!/bin/bash
# Build Metropolitan Line Variable Font with avar2

set -e  # Exit on error

echo "🔨 Building Metropolitan Line Variable Font"
echo "==========================================="

# Clean previous builds
rm -rf build/
mkdir -p build

# Step 1: Build the variable font
echo ""
echo "Step 1: Compiling variable font from designspace..."
fontmake -m MetropolitanLine.designspace \
         -o variable \
         --output-path "build/MetropolitanLine[wght].ttf" \
         --verbose WARNING

# Step 2: Generate and apply avar2 table
echo ""
echo "Step 2: Generating avar2 table from measurements..."
python3 scripts/generate_avar2.py \
    "build/MetropolitanLine[wght].ttf" \
    "build/MetropolitanLine[wght]-avar2.ttf"

# Step 3: Create test instances
echo ""
echo "Step 3: Creating test instances..."
for weight in 100 200 300 400 500 600 700 800 900; do
    echo "  Generating weight $weight..."
    fonttools varLib.instancer \
        "build/MetropolitanLine[wght]-avar2.ttf" \
        wght=$weight \
        --output "build/instances/MetropolitanLine-Weight${weight}.ttf"
done

# Step 4: Generate proof
echo ""
echo "Step 4: Generating HTML proof..."
python3 scripts/generate_proof.py

echo ""
echo "✅ Build complete!"
echo "Output files:"
ls -lh build/MetropolitanLine*.ttf
echo ""
echo "Test instances in build/instances/"
ls -lh build/instances/