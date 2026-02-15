@echo off
REM 释放端口9988并重启web服务
echo 正在检查端口9988...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr "0.0.0.0:9988" ^| findstr "LISTENING"') do (
    echo 发现占用进程 PID: %%a，正在终止...
    taskkill /F /PID %%a
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr "[::]:9988" ^| findstr "LISTENING"') do (
    echo 发现占用进程 PID: %%a，正在终止...
    taskkill /F /PID %%a 2>nul
)
echo 端口9988已释放。
echo 正在启动web服务...
conda run -n stock_env python instock/web/web_service.py
