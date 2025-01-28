@echo off
Title XConnect 1.1
setlocal

set PY_SCRIPT=main.py

net session >nul 2>&1
if %errorLevel% equ 0 (
    goto :RUN_SCRIPT
)

echo Вы не запустили скрипт от имени администратора.
echo Запустить от имени администратора? (Y/N)
set /p choice=Выберите Y или N: 

if /i "%choice%"=="Y" (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
) else (
    echo Запуск отменён.
    pause
    exit /b
)

:RUN_SCRIPT
if not exist "%~dp0x64" (
    echo Ошибка: Папка "%~dp0x64" не найдена!
    pause
    exit /b 1
)

cd /d "%~dp0x64" || (
    echo Ошибка: Не удалось перейти в папку "%~dp0x64"!
    pause
    exit /b 1
)

if not exist "%PY_SCRIPT%" (
    echo Ошибка: Файл "%PY_SCRIPT%" не найден!
    pause
    exit /b 1
)

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python не установлен или не добавлен в PATH!
    pause
    exit /b 1
)

python %PY_SCRIPT% HWID

if %errorlevel% equ 0 (
    echo Скрипт "%PY_SCRIPT%" успешно завершён.
) else (
    echo Ошибка: Не удалось выполнить скрипт "%PY_SCRIPT%" (код ошибки: %errorlevel%).
)

pause