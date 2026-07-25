
source ../tools/metropolitanline-delta-env/bin/activate

## MAKE VF

# ROMAN
fontmake -m MetropolitanLineDelta.designspace \
         -o variable \
         --output-path ../fonts/MetropolitanLineDelta-VF.ttf

echo "Done → MetropolitanLineDelta-VF.ttf (avar2)"
echo "Check VF for avar"
ttx -t avar -o - ../fonts/MetropolitanLineDelta-VF.ttf | head -30

# STATICS
#sh source
#/build-MetropolitanDelta-statics.sh

deactivate
