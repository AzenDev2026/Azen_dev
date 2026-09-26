# about_dialog.py
import os
import platform
import subprocess
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QWidget, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


# ---------- sysver.txt 解析 ----------

SYSVER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sysver.txt")


class SysVerConfig:
    """解析 sysver.txt。任何一项缺失/格式错误则 valid=False。"""

    def __init__(self):
        self.valid = False
        self.logo_path = ""
        self.name = ""
        self.version_code = ""
        self.other_path = ""    # other_info 下的 path，默认 /etc/os-release

        self._parse()

    def _parse(self):
        if not os.path.exists(SYSVER_FILE):
            return
        try:
            with open(SYSVER_FILE, "r", encoding="utf-8") as f:
                raw = f.read()
        except OSError:
            return

        # 用 {xxx} : 作为分隔符
        sections = {}
        current = None
        for line in raw.splitlines():
            line = line.rstrip()
            stripped = line.strip()
            if stripped.startswith("{") and "}" in stripped:
                # 形如 "{logo_path} :"
                end = stripped.find("}")
                key = stripped[1:end].strip()
                sections[key] = []
                current = key
                continue
            if current is not None:
                sections[current].append(line)

        # 必须有 logo_path / system_version / other_info 三个段
        if not all(k in sections for k in ("logo_path", "system_version", "other_info")):
            return

        # logo_path：第一行非空内容
        logo_lines = [l.strip() for l in sections["logo_path"] if l.strip()]
        if not logo_lines:
            return
        self.logo_path = logo_lines[0]

        # system_version：必须有 name 和 version code
        for l in sections["system_version"]:
            ls = l.strip()
            if ls.lower().startswith("name:"):
                self.name = ls.split(":", 1)[1].strip()
            elif ls.lower().startswith("version code:"):
                self.version_code = ls.split(":", 1)[1].strip()
        if not self.name or not self.version_code:
            return

        # other_info：path: xxx
        for l in sections["other_info"]:
            ls = l.strip()
            if ls.lower().startswith("path:"):
                self.other_path = ls.split(":", 1)[1].strip()
                break
        if not self.other_path:
            self.other_path = "/etc/os-release"

        # logo 文件存在性检查（不强制存在，但存在才认为完整）
        # 用户可能后续换图，这里不强制
        self.valid = True


def load_sysver() -> SysVerConfig:
    return SysVerConfig()


# ---------- 系统信息读取 ----------

def _read_os_release(path: str = "/etc/os-release") -> dict:
    try:
        return platform.freedesktop_os_release()
    except (OSError, AttributeError):
        pass
    data = {}
    for p in (path, "/etc/os-release", "/usr/lib/os-release"):
        if p and os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if "=" in line and not line.startswith("#"):
                            k, v = line.split("=", 1)
                            data[k.strip()] = v.strip().strip('"')
                break
            except OSError:
                continue
    return data


def _get_cpu_model() -> str:
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "未知"


def _get_memory_gb() -> str:
    try:
        import psutil
        return f"{psutil.virtual_memory().total / (1024**3):.1f} GiB"
    except ImportError:
        pass
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    kb = int(line.split()[1])
                    return f"{kb / (1024**2):.1f} GiB"
    except (OSError, ValueError):
        pass
    return "未知"


def _get_kde_version() -> str:
    ver = os.environ.get("KDE_SESSION_VERSION")
    if ver:
        return ver
    try:
        out = subprocess.check_output(
            ["plasmashell", "--version"],
            stderr=subprocess.DEVNULL, timeout=3
        ).decode().strip()
        return out.split()[-1] if out else "未知"
    except Exception:
        return "未知"


def _get_kernel() -> str:
    return platform.release()


def _get_gpu() -> str:
    try:
        out = subprocess.check_output(
            ["lspci"], stderr=subprocess.DEVNULL, timeout=3
        ).decode()
        for line in out.splitlines():
            if any(k in line for k in ("VGA compatible", "3D controller", "Display controller")):
                if ":" in line:
                    return line.split(":", 2)[-1].strip()
    except Exception:
        pass
    return "未知"


# ---------- 关于本机 Dialog ----------

class AboutSystemDialog(QDialog):
    def __init__(self, parent=None, strings=None):
        """strings 可选，传入 i18n.t 包装的字典，缺省用中文。"""
        super().__init__(parent)
        self.setWindowTitle("关于本机")
        self.setFixedSize(520, 480)
        self.setModal(True)

        self._t = strings or (lambda k, **kw: {
            "about": "关于本机",
            "close": "关闭",
            "config_error": "配置文件错误",
        }.get(k, k))

        cfg = load_sysver()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 16)
        outer.setSpacing(0)

        # 头部：logo + 系统名
        header = QHBoxLayout()
        header.setSpacing(14)

        logo_label = QLabel()
        logo_label.setFixedSize(56, 56)
        if cfg.valid and cfg.logo_path and os.path.exists(cfg.logo_path):
            pm = QPixmap(cfg.logo_path)
            if not pm.isNull():
                logo_label.setPixmap(pm.scaled(
                    56, 56,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                ))
        header.addWidget(logo_label)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        if cfg.valid:
            title = QLabel(cfg.name)
            title.setStyleSheet("font-size: 20px; font-weight: 600;")
            subtitle = QLabel(cfg.version_code)
            subtitle.setStyleSheet("font-size: 12px; color: #888;")
        else:
            title = QLabel(self._t("config_error"))
            title.setStyleSheet("font-size: 20px; font-weight: 600; color: #c0392b;")
            subtitle = QLabel("sysver.txt")
            subtitle.setStyleSheet("font-size: 12px; color: #888;")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box, 1)
        outer.addLayout(header)
        outer.addSpacing(16)

        # 若配置无效，直接给提示并返回
        if not cfg.valid:
            warn = QLabel(self._t("config_error"))
            warn.setStyleSheet("color: #c0392b; font-size: 13px;")
            outer.addWidget(warn)
            outer.addStretch(1)
            self._add_close_button(outer)
            return

        # 配置有效：读 os-release 展示其他信息
        os_data = _read_os_release(cfg.other_path)
        pretty_name = os_data.get("PRETTY_NAME") or os_data.get("NAME") or "Linux"
        version_id = os_data.get("VERSION_ID", "")
        os_id = os_data.get("ID", "")

        rows = [
            ("操作系统", pretty_name),
            ("系统标识", f"{os_id} {version_id}".strip()),
            ("KDE Plasma", _get_kde_version()),
            ("内核版本", _get_kernel()),
            ("处理器", _get_cpu_model()),
            ("内存", _get_memory_gb()),
            ("图形处理器", _get_gpu()),
        ]

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)

        for label_text, value_text in rows:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: palette(base);
                    border: 1px solid palette(mid);
                    border-radius: 6px;
                }
            """)
            card.setFixedHeight(56)
            h = QHBoxLayout(card)
            h.setContentsMargins(14, 8, 14, 8)

            lbl = QLabel(label_text)
            lbl.setStyleSheet("font-size: 13px; color: #888; background: transparent; border: none;")
            lbl.setFixedWidth(100)

            val = QLabel(value_text)
            val.setStyleSheet("font-size: 13px; font-weight: 500; background: transparent; border: none;")
            val.setWordWrap(True)
            val.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            h.addWidget(lbl)
            h.addWidget(val, 1)
            content_layout.addWidget(card)

        content_layout.addStretch(1)
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

        self._add_close_button(outer)

    def _add_close_button(self, outer_layout):
        from PyQt6.QtWidgets import QPushButton
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        close_btn = QPushButton(self._t("close"))
        close_btn.setFixedWidth(80)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        outer_layout.addLayout(btn_layout)