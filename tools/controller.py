# menuTitle: MetropolitanLineDelta Controller

"""RoboFont/xTools4 controller using the project's authored designspace."""

import os
from pathlib import Path
import subprocess

from fontTools.designspaceLib import DesignSpaceDocument
from xTools4.modules.xproject import xProject


class MetropolitanLineDeltaController(xProject):
    
    sourcesFolderName = 'sources'
    fontsFolderName = 'fonts'
    proofsFolderName = 'proofs'

    def __init__(self, folder=None, familyName='Metropolitan Line Delta',
                 subFamily='Roman'):
        if subFamily != 'Roman':
            raise ValueError('This project currently has only a Roman designspace.')
        if folder is None:
            folder = Path(__file__).resolve().parents[1]
        super().__init__(str(Path(folder).resolve()), familyName)
        self.subFamily = subFamily
        self.buildDesignspace()

    @property
    def designspaceFile(self):
        return 'MetropolitanLineDelta.designspace'

    @property
    def sourcesPaths(self):
        # Use registered paths, including both "-" and "_" filename separators.
        return list(dict.fromkeys(source.path for source in self.designspace.sources))

    @property
    def defaultSourcePath(self):
        return self.designspace.findDefault().path

    @property
    def varFontFile(self):
        return 'MetropolitanLineDelta-VF.ttf'

    @property
    def parametricAxes(self):
        return [axis.tag for axis in self.designspace.axes if axis.tag != 'wght']

    @property
    def defaultLocation(self):
        return self.designspace.newDefaultLocation()

    def getAxisName(self, tag):
        return next(axis.name for axis in self.designspace.axes if axis.tag == tag)

    @property
    def fontmakePython(self):
        return os.path.join(
            self.baseFolder, 'tools', 'metropolitanline-delta-env', 'bin', 'python'
        )

    def buildDesignspace(self):
        """Reload and check the authored designspace without rewriting it.

        Unlike the Computer Modern example, this project defines its axes,
        mappings and source locations directly in the designspace. Edit that
        file, then reload it here; no measurements or blends.json are required.
        """
        document = DesignSpaceDocument.fromfile(self.designspacePath)
        axes = {axis.name: axis for axis in document.axes}
        locations = set()
        for source in document.sources:
            if not source.path or not Path(source.path).is_dir():
                raise FileNotFoundError(f'Missing UFO source: {source.path}')
            unknown = set(source.location) - set(axes)
            if unknown:
                raise ValueError(f'{source.name}: unknown axes {sorted(unknown)}')
            location = source.getFullDesignLocation(document)
            for name, value in location.items():
                axis = axes[name]
                minimum = axis.map_forward(axis.minimum)
                maximum = axis.map_forward(axis.maximum)
                if not minimum <= value <= maximum:
                    raise ValueError(
                        f'{source.name}: {name}={value} outside [{minimum}, {maximum}]'
                    )
            key = tuple(location[name] for name in axes)
            if key in locations:
                raise ValueError(f'Duplicate source location: {source.name}')
            locations.add(key)
        if document.findDefault() is None:
            raise ValueError('The designspace needs a source at the default location.')
        self.designspace = document
        if self.verbose:
            print(f'Loaded {len(document.axes)} axes and {len(document.sources)} sources '
                  f'from {self.designspaceFile}')
        return document

    def buildVariableFont(self, debug=False, featureWriter=True, noGDEF=False):
        """Build with the repository's fontmake environment; propagate failures."""
        self.buildDesignspace()
        if not os.path.isfile(self.fontmakePython):
            raise FileNotFoundError(
                f'Missing build Python: {self.fontmakePython}. '
                'Create tools/metropolitanline-delta-env and install requirements.txt.'
            )
        os.makedirs(self.fontsFolder, exist_ok=True)
        command = [
            self.fontmakePython, '-m', 'fontmake',
            '-m', self.designspacePath, '-o', 'variable',
            '--output-path', self.varFontPath,
            '--keep-direction', '--verbose', 'DEBUG' if debug else 'WARNING',
        ]
        if not featureWriter:
            command.extend(['--feature-writer', 'None'])
        if noGDEF:
            command.append('--no-generate-GDEF')
        # RoboFont's embedded Python settings must not leak into the venv.
        env = os.environ.copy()
        env.pop('PYTHONHOME', None)
        env.pop('PYTHONPATH', None)
        subprocess.run(command, cwd=self.baseFolder, env=env, check=True)
        return self.varFontPath


if __name__ == '__main__':
    # Run in RoboFont with xTools4 installed. Paths are relative to this script.
    p = MetropolitanLineDeltaController()
    controlGlyphs = list('HOWTBnop')

    # Project information and source validation:
    # p.printSettings()
    # p.printAxes()
    # p.validateSources(tuning=False, reference=False)

    # Optional source operations (these modify UFOs):
    # p.copyGroupsFromDefault()
    # p.copyUnicodesFromDefault(tuning=False, reference=False)
    # p.copyGlyphOrderFromDefault(tuning=False, reference=False)

    # Proofing in RoboFont:
    # p.proofGlyphMemes(controlGlyphs, anchors=False)
    # p.proofSourcesGlyphSet(showCompatible=True, validateComposites=True)

    # Build fonts/MetropolitanLineDelta-VF.ttf using the existing mappings.
    p.buildVariableFont(debug=False, featureWriter=False)