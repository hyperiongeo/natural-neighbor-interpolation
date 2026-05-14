import platform
from setuptools import Extension, setup, find_packages
import sys
import sysconfig


def get_short_path_windows(path):
    """Convert a Windows path to short (8.3) format to avoid encoding issues with MSVC linker.

    The MSVC linker on Windows doesn't handle UTF-8 paths properly when they contain
    non-ASCII characters. Converting to short path format avoids this issue.
    """
    if platform.system() != 'Windows':
        return path

    try:
        import ctypes
        from ctypes import wintypes

        # GetShortPathNameW is the Unicode version that handles UTF-8 paths
        kernel32 = ctypes.windll.kernel32
        kernel32.GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
        kernel32.GetShortPathNameW.restype = wintypes.DWORD

        # Allocate buffer for short path (MAX_PATH = 260, but allow for longer paths)
        buffer_size = 32767
        buffer = ctypes.create_unicode_buffer(buffer_size)

        # Convert input path to Unicode
        result = kernel32.GetShortPathNameW(path, buffer, buffer_size)

        if result == 0 or result >= buffer_size:
            # If GetShortPathName fails or buffer too small, return original path
            return path

        return buffer.value
    except (ImportError, OSError, AttributeError):
        # If ctypes or Windows API call fails, return original path
        return path


def get_extension():
    """Build the C++ extension with platform-specific compile arguments."""
    # Import numpy here (only when actually building)
    import numpy

    # Platform-specific compile arguments and library directories
    if platform.system() == 'Windows':
        # MSVC compiler flags
        extra_compile_args = ['/std:c++14', '/O2']
        # On Windows, explicitly specify Python library directory to help linker find python*.lib
        # This is especially important for tox environments and paths with non-ASCII characters
        import os
        # Use sys.prefix (Python installation root) to construct libs path
        # This is more reliable than sysconfig.get_config_var('LIBDIR') which can be relative
        python_prefix = sys.prefix
        lib_dir = os.path.join(python_prefix, 'libs')
        # Verify the directory exists and contains python*.lib
        if os.path.isdir(lib_dir) and any(f.startswith('python') and f.endswith('.lib') for f in os.listdir(lib_dir)):
            # Convert to short path format to avoid MSVC linker encoding issues with non-ASCII paths
            lib_dir = get_short_path_windows(lib_dir)
            library_dirs = [lib_dir]
        else:
            # Fallback: try sysconfig.get_config_var, but make it absolute
            lib_dir = sysconfig.get_config_var('LIBDIR')
            if lib_dir and not os.path.isabs(lib_dir):
                # If relative, make it absolute relative to prefix
                lib_dir = os.path.join(python_prefix, lib_dir)
            if lib_dir and os.path.isdir(lib_dir):
                # Convert to short path format to avoid MSVC linker encoding issues
                lib_dir = get_short_path_windows(lib_dir)
                library_dirs = [lib_dir]
            else:
                # Last resort: empty list (let setuptools try auto-detection)
                library_dirs = []
    else:
        # GCC/Clang compiler flags
        extra_compile_args = ['--std=c++11', '-O3']
        library_dirs = []  # No external libraries needed on Unix

    return Extension(
        'cnaturalneighbor',
        include_dirs=[numpy.get_include()],
        library_dirs=library_dirs,
        extra_compile_args=extra_compile_args,
        sources=[
            'naturalneighbor/cnaturalneighbor.cpp',
        ],
    )


# Only build extension if we're actually building (not just getting metadata)
# This allows metadata commands to work without numpy installed
# Commands that need the extension built
# Note: 'sdist' should NOT be here - it only packages source, doesn't build
build_commands = ['build', 'build_ext', 'install', 'develop', 'bdist', 'bdist_wheel']
# Commands that are metadata-only
metadata_commands = ['egg_info', 'clean', '--version', '--help-commands']

# Check if we're running a build command (and not a metadata-only command)
needs_build = any(cmd in sys.argv for cmd in build_commands)
is_metadata_only = any(cmd in sys.argv for cmd in metadata_commands)

if needs_build and not is_metadata_only:
    # All package metadata (name, version, description, etc.) is defined in pyproject.toml.
    # setuptools reads that metadata automatically; here we only add the compiled extension.
    setup(ext_modules=[get_extension()])
else:
    # For metadata-only commands, don't require numpy.
    # Metadata is still taken from pyproject.toml via setuptools.
    setup(
    name='your_package_name',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',  # Example dependency
    ],
)
