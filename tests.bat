@echo off

set "PY=C:\work\Repositories\bybit\first\Scripts\python.exe"
set "SCRIPT=C:\work\Repositories\bybit\tests_usdt.py"


wt -w 0 nt cmd /k "echo XRP/USDT && %PY% %SCRIPT% -s XRPUSDT" ^
; split-pane -H cmd /k "echo BTC/USDT && %PY% %SCRIPT% -s BTCUSDT" ^
; move-focus up ^
; split-pane -V cmd /k "echo ETH/USDT && %PY% %SCRIPT% -s ETHUSDT" ^
; move-focus down ^
; split-pane -V cmd /k "echo SOL/USDT && %PY% %SCRIPT% -s SOLUSDT"
