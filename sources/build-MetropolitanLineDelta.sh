
source ../tools/metropolitanline-delta-env/bin/activate

## MAKE VF

# ROMAN
fontmake -m MetropolitanLineDelta.designspace -o variable --output-path ../fonts/MetropolitanLineDelta-VF.ttf --no-production-names --no-check-compatibility
echo "Done → MetropolitanLineDelta-VF.ttf"

# STATICS
#sh source

# Apply non-linear avar2
python3 ../tools/apply-avar1.py ../fonts/MetropolitanLineDelta-VF.ttf
echo "Done → applying avar1"

#/build-MetropolitanDelta-statics.sh

deactivate
