@echo off
Title XConnect 1.1
setlocal

set PY_SCRIPT=main.py

net session >nul 2>&1
if %errorLevel% equ 0 (
    goto :RUN_SCRIPT
)

echo �� �� �����⨫� �ਯ� �� ����� �����������.
echo �������� �� ����� �����������? (Y/N)
set /p choice=�롥�� Y ��� N: 

if /i "%choice%"=="Y" (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
) else (
    echo ����� �⬥��.
    pause
    exit /b
)

:RUN_SCRIPT
if not exist "%~dp0x64" (
    echo �訡��: ����� "%~dp0x64" �� �������!
    pause
    exit /b 1
)

cd /d "%~dp0x64" || (
    echo �訡��: �� 㤠���� ��३� � ����� "%~dp0x64"!
    pause
    exit /b 1
)

if not exist "%PY_SCRIPT%" (
    echo �訡��: ���� "%PY_SCRIPT%" �� ������!
    pause
    exit /b 1
)

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo �訡��: Python �� ��⠭����� ��� �� �������� � PATH!
    pause
    exit /b 1
)

python %PY_SCRIPT% HWID

if %errorlevel% equ 0 (
    echo ��ਯ� "%PY_SCRIPT%" �ᯥ譮 �������.
) else (
    echo �訡��: �� 㤠���� �믮����� �ਯ� "%PY_SCRIPT%" (��� �訡��: %errorlevel%).
)

pause