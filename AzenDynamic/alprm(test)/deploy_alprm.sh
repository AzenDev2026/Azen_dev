#!/bin/bash
# ================================================================
#  ALPRM Monitor - Deploy Script
#  Azen Laptop Power Resources Management
#  Supports: Arch Linux / Ubuntu / Debian
# ================================================================

set -e

# ---------- 颜色 ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()   { echo -e "${RED}[ERROR]${NC} $1"; }

# ---------- 检查 root ----------
if [[ $EUID -ne 0 ]]; then
    err "此脚本需要 root 权限运行"
    echo "请使用: sudo ./deploy_alprm.sh"
    exit 1
fi

# ---------- 识别发行版 ----------
detect_distro() {
    if [ -f /etc/arch-release ]; then
        echo "arch"
    elif [ -f /etc/debian_version ]; then
        # 进一步区分 Debian / Ubuntu
        if grep -qi "ubuntu" /etc/os-release 2>/dev/null; then
            echo "ubuntu"
        else
            echo "debian"
        fi
    else
        echo "unknown"
    fi
}

DISTRO=$(detect_distro)
info "检测到发行版: $DISTRO"

# ---------- 定位项目根目录 ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
info "项目目录: $SCRIPT_DIR"

if [ ! -f "Makefile" ]; then
    err "未找到 Makefile，请确认你在 alprm-monitor/ 目录下"
    exit 1
fi

# ---------- 1. 检查并安装依赖 ----------
info "检查编译依赖..."

install_deps_arch() {
    local pkgs=()
    command -v gcc  &>/dev/null || pkgs+=("gcc")
    command -v make &>/dev/null || pkgs+=("make")
    [ -f /usr/include/systemd/sd-bus.h ] || pkgs+=("systemd-libs")

    if [ ${#pkgs[@]} -ne 0 ]; then
        warn "缺少依赖: ${pkgs[*]}"
        info "通过 pacman 安装..."
        pacman -S --needed --noconfirm "${pkgs[@]}"
    fi
}

install_deps_debian() {
    local pkgs=()
    command -v gcc  &>/dev/null || pkgs+=("gcc")
    command -v make &>/dev/null || pkgs+=("make")
    [ -f /usr/include/systemd/sd-bus.h ] || pkgs+=("libsystemd-dev")

    if [ ${#pkgs[@]} -ne 0 ]; then
        warn "缺少依赖: ${pkgs[*]}"
        info "通过 apt 安装..."
        apt update
        apt install -y "${pkgs[@]}"
    fi
}

case "$DISTRO" in
    arch)
        install_deps_arch
        ;;
    ubuntu|debian)
        install_deps_debian
        ;;
    *)
        warn "未知发行版，跳过自动依赖安装"
        warn "请手动确保已安装: gcc, make, libsystemd-dev"
        ;;
esac

ok "依赖检查完成"

# ---------- 2. 编译 ----------
info "开始编译..."
make clean > /dev/null 2>&1 || true

if make; then
    ok "编译成功"
else
    err "编译失败，请检查上方错误信息"
    exit 1
fi

if [ ! -f "alprm-monitor" ]; then
    err "未生成 alprm-monitor 二进制文件"
    exit 1
fi

# ---------- 3. 安装二进制 ----------
info "安装到系统..."
make install
ok "二进制已安装到 /usr/local/bin/alprm-monitor"

# ---------- 4. 安装 systemd 服务 ----------
if [ -f "systemd/alprm-monitor.service" ]; then
    info "安装 systemd 服务..."
    cp systemd/alprm-monitor.service /etc/systemd/system/
    systemctl daemon-reload
    ok "systemd 服务已安装"
else
    warn "未找到 systemd/alprm-monitor.service，跳过"
fi

# ---------- 5. 创建日志目录 ----------
if [ ! -d "/etc/ALPRM_log" ]; then
    mkdir -p /etc/ALPRM_log
    chmod 755 /etc/ALPRM_log
    ok "日志目录已创建: /etc/ALPRM_log"
else
    ok "日志目录已存在: /etc/ALPRM_log"
fi

# ---------- 6. 询问是否启用服务 ----------
echo
read -p "是否立即启用并启动 ALPRM Monitor 服务？(y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    systemctl enable --now alprm-monitor.service
    sleep 1
    if systemctl is-active --quiet alprm-monitor.service; then
        ok "服务已启动并设为开机自启"
    else
        err "服务启动失败，请运行: journalctl -u alprm-monitor.service -n 50"
    fi
else
    info "跳过服务启动"
    echo "  稍后可手动运行:"
    echo "    sudo systemctl enable --now alprm-monitor.service"
fi

# ---------- 7. 完成 ----------
echo
echo "================================================================"
ok " 🎉 ALPRM Monitor 部署完成！"
echo "================================================================"
echo
echo "  二进制位置:  /usr/local/bin/alprm-monitor"
echo "  日志文件:    /etc/ALPRM_log/events.log"
echo "  服务名称:    alprm-monitor.service"
echo
echo "  常用命令:"
echo "    查看状态:  sudo systemctl status alprm-monitor"
echo "    查看日志:  sudo journalctl -u alprm-monitor -f"
echo "    事件日志:  sudo tail -f /etc/ALPRM_log/events.log"
echo "    停止服务:  sudo systemctl stop alprm-monitor"
echo
echo "  手动运行（不走服务）:"
echo "    sudo /usr/local/bin/alprm-monitor"
echo
echo "================================================================"
