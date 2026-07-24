
source ../tools/metropolitanline-delta-env/bin/activate

## MAKE VF

# ROMAN
fontmake -m MetropolitanLineDelta.designspace -o variable --output-path ../fonts/MetropolitanLineDelta-VF.ttf --no-production-names --no-check-compatibility
echo "Done → MetropolitanLineDelta-VF.ttf"

# STATICS
#sh source
#/build-MetropolitanDelta-statics.sh

deactivate
