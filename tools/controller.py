# menuTitle: MetropolitanLineDelta Controller

from importlib import reload
import xTools4.modules.xproject
reload(xTools4.modules.xproject)

import os, shutil
from xTools4.modules.xproject import *


class MetropolitanLineDeltaController(xProject):
    
    _parametricAxes = {
        'Roman'  : ['XTSP', 'XOPQ', 'YOPQ', 'XOUC', 'XOLC', 'YOUC', 'YOLC', 'STUI', 'STUO', 'XTRA', 'XTUC', 'XTLC', 'YOMB', 'YTDE', 'INKT'],
    }

    # parametric axes with arbitrary scales
    #_customParametricAxes = {
    #    'GRAD' : 0,
    #}

    def __init__(self, folder, familyName, subFamily):
        self.baseFolder = folder
        self.familyName = familyName
        self.subFamily  = subFamily

    @property
    def designspaceFile(self):
        return f"{self.subFamily.replace(' ', '')}.designspace"

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, self.sourcesFolderName, self.subFamily)

    @property
    def defaultSourcePath(self):
        return os.path.join(self.sourcesFolder, f"{self.subFamily.replace(' ', '')}_{self.defaultName}.ufo")

    @property
    def varFontFile(self):
        fileName = f"{self.familyName}-{self.subFamily}_avar2.ttf"
        return fileName.replace(' ', '')

    @property
    def referenceBlendsPath(self):
        return os.path.join(self.sourcesFolder, 'reference', self.blendsFile)

    @property
    def referenceFontPath(self):
        return os.path.join(self.fontsFolder, 'reference', f"{self.familyName.replace(' ', '')}-{self.subFamily}.ttf")

    @property
    def parametricAxes(self):
        return self._parametricAxes[self.subFamily]

    @property
    def defaultLocation(self):
        location = super().defaultLocation.copy()
        location['Grades'] = 0
        return location

    def buildBlendsFile(self):
        if self.verbose:
            print('\tbuilding blends file...')
        if os.path.exists(self.blendsPath):
            os.remove(self.blendsPath)
        shutil.copy(self.referenceBlendsPath, self.blendsPath)

    def patchBlendsFile(self):

        # import blends data
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsDict = json.load(f)

        # import & apply patch data
        patchPath = self.blendsPath.replace('.json', '_patch.json')
        if not os.path.exists(patchPath):
            return

        with open(patchPath, 'r', encoding='utf-8') as f:
            patchDict = json.load(f)

        for key1, value1 in patchDict.items():
            if key1 not in blendsDict:
                print(f'{key1} not in blends dict')
                continue
            for key2, value2 in value1.items():
                if key2 not in blendsDict[key1]:
                    blendsDict[key1][key2] = {}
                for k, v in value2.items():
                    blendsDict[key1][key2][k] = v

        # save patched blends data
        with open(self.blendsPath, 'w', encoding='utf-8') as f:
            json.dump(blendsDict, f, indent=2)

    def buildDesignspace(self, patchBlends=True, tuning=False, instances=False):
        if self.verbose:
            print(f'building {os.path.split(self.designspacePath)[-1]}...')

        self.buildBlendsFile()
        if patchBlends:
            self.patchBlendsFile()

        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes(self._customParametricAxes)
        self.addBlendedSources()
        self.addDefaultSource()
        self.addParametricSources()
        self.addCustomKeysToLib()
        self.save()

    def setSourceNamesFromMeasurements(self, preflight=True, ignoreTags=['wght']):
        setSourceNamesFromMeasurements(
                self.sourcesFolder,
                self.subFamily,
                self.measurementsPath,
                preflight=preflight,
                ignoreTags=ignoreTags,
                infoFamilyName=f'{self.familyName} {self.subFamily}',
        )


if __name__ == '__main__':

    folder = os.path.dirname(os.getcwd())

    subFamily = ['Roman'][1]

    controlGlyphs = list('HOVTDnovdp')
    # controlGlyphs += ['zero', 'one', 'period']

    p = MetropolitanLineDeltaController(folder, 'Metropolitan Line Delta', subFamily)

    #--- sources ---
    # p.createParametricSources(['XQAC', 'YQAC'], minSource=True, maxSource=True)
    # p.setSourceNamesFromMeasurements(preflight=False)

    #--- copy from default ---
    # p.updateGlyphsFromDefault(glyphNames, 'WDSP1000', preflight=True)
    # p.copyGlyphsFromDefault(glyphNames)
    # p.copyGroupsFromDefault()
    # p.copyUnicodesFromDefault(preflight=True)
    # p.copyGlyphOrderFromDefault()
    # p.buildCompositeGlyphs(glyphNames)

    #--- normalization --- 
    # p.cleanupSources(parametric=True, tuning=False, clearFontGuides=True, clearGlyphGuides=True, clearMarks=True, clearLayers=True, ignoreLayers=[])
    # p.normalizeSources(parametric=True, tuning=False)

    #--- build designspace ---
    p.parametricAxesHidden = True
    p.buildDesignspace(patchBlends=False)
    # p.validateDesignspace(locations=True, mappings=True, instances=False)
    # p.validateSources()

    #--- project info
    # p.printSettings()
    # p.printAxes()

    #--- proofing ---
    # p.proofGlyphMemes(controlGlyphs, anchors=False) # controlGlyphs
    # p.proofSourcesGlyphSet(showCompatible=True, validateComposites=True)
    # p.proofBlends(controlGlgit sytatuyphs, levelsShow=[2], points=False)

    #--- build fonts
    p.buildVariableFont(debug=False, featureWriter=False)
    # p.buildInstancesVariableFont(clear=True, ufo=True)