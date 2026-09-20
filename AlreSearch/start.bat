@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
title AlreSearch Launcher

echo ============================================
echo            AlreSearch 启动器
echo ============================================
echo.

REM ---- 切换到脚本所在目录 ----
cd /d "%~dp0"

REM ---- 检查 Java 是否安装 ----
where java >nul 2>nul
if errorlevel 1 (
    echo [错误] 未检测到 Java，请先安装 JDK 17 或更高版本。
    echo 下载地址: https://www.oracle.com/java/technologies/downloads/
    echo.
    pause
    exit /b 1
)

REM ---- 检查 javac 是否可用（需要 JDK 而非 JRE）----
where javac >nul 2>nul
if errorlevel 1 (
    echo [错误] 未检测到 javac，请安装 JDK（不是 JRE）。
    echo.
    pause
    exit /b 1
)

REM ---- 打印 Java 版本 ----
for /f "tokens=3" %%v in ('java -version 2^>^&1 ^| findstr /i "version"') do (
    set JAVA_VER=%%v
)
echo [信息] 检测到 Java 版本: !JAVA_VER!
echo.

REM ---- 准备输出目录 ----
if not exist "out" mkdir "out"

REM ---- 收集所有 .java 文件 ----
set SOURCES_FILE=%TEMP%\alresearch_sources.txt
if exist "%SOURCES_FILE%" del "%SOURCES_FILE%"
for /r "src" %%f in (*.java) do echo "%%f" >> "%SOURCES_FILE%"

REM ---- 编译 ----
echo [1/2] 正在编译源码...
javac -encoding UTF-8 -d out @"%SOURCES_FILE%"
if errorlevel 1 (
    echo.
    echo [错误] 编译失败，请检查上面的报错信息。
    del "%SOURCES_FILE%" >nul 2>nul
    pause
    exit /b 1
)
del "%SOURCES_FILE%" >nul 2>nul
echo [1/2] 编译完成。
echo.

REM ---- 运行 ----
echo [2/2] 正在启动 AlreSearch...
echo.
java -Xmx1g -cp out com.alre.Main

REM ---- 程序退出后暂停 ----
echo.
echo AlreSearch 已退出。
pause
endlocal