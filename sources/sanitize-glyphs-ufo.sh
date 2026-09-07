#!/bin/bash
#
# sanitize-glyphs-ufo.sh
#
# Removes Glyphs-app-specific metadata from a UFO that was opened and saved
# in Glyphs. Does NOT modify features.fea or glyph outlines.
#
# Usage:
#   ./sanitize-glyphs-ufo.sh <ufo_to_clean>
#

set -e

UFO_PATH="$1"

if [ -z "$UFO_PATH" ]; then
    echo "Usage: $0 <ufo_to_clean>"
    exit 1
fi

if [ ! -d "$UFO_PATH" ]; then
    echo "Error: $UFO_PATH is not a directory"
    exit 1
fi

UFO_NAME=$(basename "$UFO_PATH")
echo "Sanitizing: $UFO_NAME"

# ---------------------------------------------------------------------------
# 1. Clean lib.plist: remove all com.schriftgestaltung.* keys
# ---------------------------------------------------------------------------
LIB_PLIST="$UFO_PATH/lib.plist"
if [ -f "$LIB_PLIST" ]; then
    echo "  Cleaning lib.plist..."
    python3 - "$LIB_PLIST" << 'PYEOF'
import plistlib
import sys

def remove_schriftgestaltung(d):
    if isinstance(d, dict):
        return {
            k: remove_schriftgestaltung(v)
            for k, v in d.items()
            if not k.startswith("com.schriftgestaltung.")
        }
    elif isinstance(d, list):
        return [remove_schriftgestaltung(item) for item in d]
    return d

path = sys.argv[1]
with open(path, 'rb') as f:
    data = plistlib.load(f)
cleaned = remove_schriftgestaltung(data)
with open(path, 'wb') as f:
    plistlib.dump(cleaned, f, sort_keys=False)
PYEOF
fi

# ---------------------------------------------------------------------------
# 2. Clean .glif files: remove com.schriftgestaltung.* keys from <lib> sections
# ---------------------------------------------------------------------------
echo "  Cleaning .glif lib sections..."
find "$UFO_PATH" -name "*.glif" -print0 | while IFS= read -r -d '' glif; do
    python3 - "$glif" << 'PYEOF'
import sys
import xml.etree.ElementTree as ET

path = sys.argv[1]
tree = ET.parse(path)
root = tree.getroot()
changed = False

for lib in root.findall('.//lib'):
    for dict_elem in list(lib.findall('dict')):
        children = list(dict_elem)
        i = 0
        while i < len(children):
            elem = children[i]
            if elem.tag == 'key' and elem.text and elem.text.startswith('com.schriftgestaltung.'):
                # remove the key
                dict_elem.remove(elem)
                # remove its associated value element
                if i < len(list(dict_elem)):
                    value_elem = list(dict_elem)[i]
                    dict_elem.remove(value_elem)
                changed = True
                children = list(dict_elem)
            else:
                i += 1

if changed:
    # write back preserving declaration
    tree.write(path, encoding='UTF-8', xml_declaration=True)
PYEOF
done

# ---------------------------------------------------------------------------
# 3. Optionally remove Glyphs creator from metainfo.plist
#     (Commented out by default — keep it if you want to track the export tool)
# ---------------------------------------------------------------------------
# METAINFO="$UFO_PATH/metainfo.plist"
# if [ -f "$METAINFO" ]; then
#     python3 - "$METAINFO" << 'PYEOF'
# import plistlib
# import sys
# path = sys.argv[1]
# with open(path, 'rb') as f:
#     data = plistlib.load(f)
# data.pop('creator', None)
# with open(path, 'wb') as f:
#     plistlib.dump(data, f)
# PYEOF
# fi

echo "Done: $UFO_NAME sanitized."
