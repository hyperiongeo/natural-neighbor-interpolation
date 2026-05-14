import sys
import os
import glob

# Add build directory to Python path for editable installs
# This allows the compiled extension to be found when installed in editable mode
_package_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_package_dir)
_build_dir = os.path.join(_project_root, 'build')

# Find the platform-specific build directory (e.g., lib.win-amd64-cpython-314)
if os.path.isdir(_build_dir):
    for item in os.listdir(_build_dir):
        build_lib_path = os.path.join(_build_dir, item)
        if os.path.isdir(build_lib_path) and item.startswith('lib.'):
            # Check if the extension exists in this build directory
            # Extension files can have various suffixes like .cp314-win_amd64.pyd
            ext_files = glob.glob(os.path.join(build_lib_path, 'cnaturalneighbor.*'))
            # Filter for actual extension files (.pyd on Windows, .so on Unix)
            ext_files = [f for f in ext_files if f.endswith(('.pyd', '.so'))]
            if ext_files:
                if build_lib_path not in sys.path:
                    sys.path.insert(0, build_lib_path)
                break

from .naturalneighbor import griddata

__all__ = [
    'griddata',
]
