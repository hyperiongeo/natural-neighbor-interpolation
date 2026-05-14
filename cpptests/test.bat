@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"
if not exist build mkdir build
cd build

REM Check if cmake is available in PATH
where cmake >nul 2>&1
if errorlevel 1 (
    REM Try to find cmake in conda environment
    set "CMAKE="
    if defined CONDA_PREFIX (
        if exist "%CONDA_PREFIX%\Library\bin\cmake.exe" (
            set "CMAKE=%CONDA_PREFIX%\Library\bin\cmake.exe"
        ) else if exist "%CONDA_PREFIX%\bin\cmake.exe" (
            set "CMAKE=%CONDA_PREFIX%\bin\cmake.exe"
        )
    )
    
    if not defined CMAKE (
        echo Error: cmake not found in PATH or conda environment
        if defined CONDA_PREFIX echo CONDA_PREFIX=%CONDA_PREFIX%
        exit /b 1
    )
) else (
    set "CMAKE=cmake"
)

%CMAKE% .. 
if errorlevel 1 exit /b 1
%CMAKE% --build . --target cpptests
if errorlevel 1 exit /b 1

set "EXE=Debug\cpptests.exe"
if not exist "%EXE%" (
    echo Error: cpptests executable not found at %EXE%
    exit /b 1
)

"%EXE%"

