#!/usr/bin/env bash
set -e

# ---- 切换到脚本所在目录 ----
cd "$(dirname "$0")"

echo "============================================"
echo "           AlreSearch 启动器"
echo "============================================"
echo

# ---- 颜色定义 ----
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

# ---- 检查 java ----
if ! command -v java >/dev/null 2>&1; then
    echo -e "${RED}[错误]${NC} 未检测到 Java，请先安装 JDK 17 或更高版本。"
    echo "  Ubuntu/Debian:  sudo apt install openjdk-17-jdk"
    echo "  CentOS/RHEL:    sudo yum install java-17-openjdk-devel"
    echo "  macOS:          brew install openjdk@17"
    exit 1
fi

# ---- 检查 javac ----
if ! command -v javac >/dev/null 2>&1; then
    echo -e "${RED}[错误]${NC} 未检测到 javac，请安装 JDK（不是 JRE）。"
    exit 1
fi

# ---- 打印 Java 版本 ----
JAVA_VER=$(java -version 2>&1 | head -n1)
echo -e "${GREEN}[信息]${NC} $JAVA_VER"
echo

# ---- 准备输出目录 ----
mkdir -p out

# ---- 收集所有 .java 文件 ----
echo "[1/2] 正在编译源码..."
find src -name "*.java" > /tmp/alresearch_sources.txt

if ! javac -encoding UTF-8 -d out @/tmp/alresearch_sources.txt; then
    echo -e "${RED}[错误]${NC} 编译失败，请检查上面的报错信息。"
    rm -f /tmp/alresearch_sources.txt
    exit 1
fi
rm -f /tmp/alresearch_sources.txt
echo -e "${GREEN}[1/2]${NC} 编译完成。"
echo

# ---- 运行 ----
echo "[2/2] 正在启动 AlreSearch..."
echo
java -Xmx1g -cp out com.alre.Main

echo
echo "AlreSearch 已退出。"