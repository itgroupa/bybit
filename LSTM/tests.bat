@echo off

set "PY=C:\work\Repositories\bybit\first\Scripts\python.exe"
set "SCRIPT=C:\work\Repositories\bybit\LSTM\tests_usdt.py"


wt -w 0 nt cmd /k "echo XRP/USDT && %PY% %SCRIPT% -s XRPUSDT -tt Hard" ^
; split-pane -H cmd /k "echo BTC/USDT && %PY% %SCRIPT% -s BTCUSDT -tt Hard" ^
; move-focus up ^
; split-pane -V cmd /k "echo ETH/USDT && %PY% %SCRIPT% -s ETHUSDT -tt Common" ^
; move-focus down ^
; split-pane -V cmd /k "echo SOL/USDT && %PY% %SCRIPT% -s SOLUSDT -tt Common"
