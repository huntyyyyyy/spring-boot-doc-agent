@echo off
REM Windows launcher for the local grading pack - use this from IntelliJ Run,
REM not the Markdown play button (that uses cmd and chokes on ## headings).
REM Requires Git for Windows. Forwards args to run_local_grading_pack.sh.
setlocal EnableExtensions

set "SCRIPT_DIR=%~dp0"
set "BASH="

if defined GIT_BASH (
  set "BASH=%GIT_BASH%"
) else if exist "C:\Program Files\Git\bin\bash.exe" (
  set "BASH=C:\Program Files\Git\bin\bash.exe"
) else if exist "C:\Program Files\Git\usr\bin\bash.exe" (
  set "BASH=C:\Program Files\Git\usr\bin\bash.exe"
)

if not defined BASH (
  echo error: Git Bash not found. Install Git for Windows or set GIT_BASH=...bash.exe
  exit /b 2
)

"%BASH%" "%SCRIPT_DIR%run_local_grading_pack.sh" %*
exit /b %ERRORLEVEL%
