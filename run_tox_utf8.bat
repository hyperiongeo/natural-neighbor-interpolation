@echo off
REM This script sets UTF-8 encoding environment variables to fix tox issues
REM when working with Chinese characters in file paths
REM Without these variables, tox writes logs in CP936 (GBK) but reads as UTF-8,
REM causing UnicodeDecodeError. PYTHONUTF8=1 forces Python to use UTF-8 encoding.
REM
REM Usage examples:
REM   run_tox_utf8.bat                    - Run all environments
REM   run_tox_utf8.bat -e py313           - Run only Python 3.13
REM   run_tox_utf8.bat -e py39,py310     - Run Python 3.9 and 3.10
REM   run_tox_utf8.bat -e py312 --recreate - Recreate environment and run Python 3.12
REM   run_tox_utf8.bat -l                 - List all available environments
REM
REM Available Python versions: py39, py310, py311, py312, py313, py314

REM Set Windows code page to UTF-8 (65001) to ensure all subprocesses use UTF-8
chcp 65001 >nul 2>&1

REM Set Python encoding environment variables
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

REM Run tox with all arguments passed through
tox %*

