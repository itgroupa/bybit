@echo off
setlocal enabledelayedexpansion

"PY=C:\work\Repositories\bybit\first\Scripts\pip" install --upgrade certifi

echo.
echo With Training? [Y/N]
choice /c yn /n /m "Y (Yes) N (No): "

if errorlevel 2 (
    set "work_flag="
) else (
    set "work_flag=-w"
)

set "PY=C:\work\Repositories\bybit\first\Scripts\python.exe"
set "SCRIPT=C:\work\Repositories\bybit\LSTM\main_usdt.py"


wt -w 0 nt cmd /k "echo XRP/USDT && %PY% %SCRIPT% -s XRPUSDT %work_flag% -tt Hard" ^
; split-pane -H cmd /k "echo BTC/USDT && %PY% %SCRIPT% -s BTCUSDT %work_flag% -tt Hard" ^
; move-focus up ^
; split-pane -V cmd /k "echo ETH/USDT && %PY% %SCRIPT% -s ETHUSDT %work_flag% -tt Common" ^
; move-focus down ^
; split-pane -V cmd /k "echo SOL/USDT && %PY% %SCRIPT% -s SOLUSDT %work_flag% -tt Common"
