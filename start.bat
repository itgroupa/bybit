C:\work\Repositories\bybit\first\Scripts\pip install --upgrade certifi

@echo off
wt -w 0 nt cmd /k "echo XRP/USDT prices && C:\work\Repositories\bybit\first\Scripts\python.exe C:\work\Repositories\bybit\main_usdt.py -s XRPUSDT" ^
; split-pane -H cmd /k "echo BTC/USDT prices && C:\work\Repositories\bybit\first\Scripts\python.exe C:\work\Repositories\bybit\main_usdt.py -s BTCUSDT" ^
; move-focus up ^
; split-pane -V cmd /k "echo ETH/USDT prices && C:\work\Repositories\bybit\first\Scripts\python.exe C:\work\Repositories\bybit\main_usdt.py -s ETHUSDT" ^
; move-focus down ^
; split-pane -V cmd /k "echo SOL/USDT prices && C:\work\Repositories\bybit\first\Scripts\python.exe C:\work\Repositories\bybit\main_usdt.py -s SOLUSDT"

