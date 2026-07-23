
source tools/metropolitan-delta-env/bin/activate

## MAKE VF

# ROMAN
fontmake -m source/Alpha/MetropolitanLine-Regular.designspace -o variable --output-path fonts/Alpha/MetropolitanLineDelta-Roman-VF.ttf --no-production-names --no-check-compatibility

# STATICS
#sh source/build-MetropolitanDelta-statics.sh

deactivate
