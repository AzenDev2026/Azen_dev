# style.py

LIGHT_QSS = """
QWidget {
    background-color: #f3f3f3;
    color: #1a1a1a;
    font-family: "Segoe UI", "Noto Sans CJK SC", "Noto Sans JP",
                 "Noto Sans", "Microsoft YaHei", sans-serif;
    font-size: 14px;
}

/* 左侧边栏 */
#Sidebar {
    background-color: #eaeaea;
    border-right: 1px solid #e0e0e0;
}
#SidebarTitle {
    font-size: 20px;
    font-weight: 600;
    padding: 20px 20px 12px 20px;
    color: #1a1a1a;
}
QPushButton#NavButton {
    text-align: left;
    padding: 10px 16px;
    margin: 2px 8px;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: #1a1a1a;
    font-size: 14px;
}
QPushButton#NavButton:hover { background-color: #dcdcdc; }
QPushButton#NavButton:checked {
    background-color: #ffffff;
    font-weight: 600;
}
QPushButton#NavButton:checked:hover { background-color: #ffffff; }

/* 右侧内容区 */
#ContentArea { background-color: #f3f3f3; }
#CategoryTitle {
    font-size: 26px;
    font-weight: 600;
    padding: 24px 32px 4px 32px;
    color: #1a1a1a;
}
#CategorySubtitle {
    font-size: 13px;
    color: #6b6b6b;
    padding: 0 32px 16px 32px;
}

/* 设置卡片 */
QFrame#SettingCard {
    background-color: #ffffff;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
}
QFrame#SettingCard:hover {
    background-color: #fafafa;
    border: 1px solid #d0d0d0;
}
QLabel#CardTitle {
    font-size: 14px;
    font-weight: 600;
    color: #1a1a1a;
    background: transparent;
}
QLabel#CardDesc {
    font-size: 12px;
    color: #6b6b6b;
    background: transparent;
}
QLabel#CardIcon { background: transparent; }

/* 通用控件 */
QPushButton {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    padding: 6px 14px;
    color: #1a1a1a;
}
QPushButton:hover { background-color: #f5f5f5; }
QPushButton:pressed { background-color: #e8e8e8; }
QPushButton:disabled { color: #a0a0a0; background-color: #f0f0f0; }

QLineEdit, QComboBox, QSpinBox {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    padding: 4px 8px;
    color: #1a1a1a;
}
QComboBox::drop-down { border: none; width: 20px; }

QCheckBox {
    spacing: 8px;
    color: #1a1a1a;
    background: transparent;
}
QCheckBox::indicator {
    width: 18px; height: 18px;
    border-radius: 4px;
    border: 1px solid #c0c0c0;
    background-color: #ffffff;
}
QCheckBox::indicator:checked {
    background-color: #0067c0;
    border: 1px solid #0067c0;
}

QSlider::groove:horizontal {
    height: 4px;
    background: #d0d0d0;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #0067c0;
    width: 16px; height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}

QListWidget {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 4px;
}
QListWidget::item {
    padding: 8px 10px;
    border-radius: 4px;
}
QListWidget::item:selected {
    background-color: #0067c0;
    color: #ffffff;
}
QListWidget::item:hover {
    background-color: #eef4fb;
}
QListWidget::item:selected:hover {
    background-color: #005ba8;
    color: #ffffff;
}

QDialog { background-color: #f3f3f3; }

QScrollArea { border: none; background: transparent; }
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px;
}
QScrollBar::handle:vertical {
    background: #c8c8c8;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: #a8a8a8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
"""


DARK_QSS = """
QWidget {
    background-color: #202020;
    color: #e8e8e8;
    font-family: "Segoe UI", "Noto Sans CJK SC", "Noto Sans JP",
                 "Noto Sans", "Microsoft YaHei", sans-serif;
    font-size: 14px;
}

#Sidebar {
    background-color: #1a1a1a;
    border-right: 1px solid #2d2d2d;
}
#SidebarTitle {
    font-size: 20px;
    font-weight: 600;
    padding: 20px 20px 12px 20px;
    color: #f0f0f0;
}
QPushButton#NavButton {
    text-align: left;
    padding: 10px 16px;
    margin: 2px 8px;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: #e8e8e8;
    font-size: 14px;
}
QPushButton#NavButton:hover { background-color: #2d2d2d; }
QPushButton#NavButton:checked {
    background-color: #333333;
    font-weight: 600;
}
QPushButton#NavButton:checked:hover { background-color: #333333; }

#ContentArea { background-color: #202020; }
#CategoryTitle {
    font-size: 26px;
    font-weight: 600;
    padding: 24px 32px 4px 32px;
    color: #f0f0f0;
}
#CategorySubtitle {
    font-size: 13px;
    color: #a0a0a0;
    padding: 0 32px 16px 32px;
}

QFrame#SettingCard {
    background-color: #2b2b2b;
    border: 1px solid #383838;
    border-radius: 8px;
}
QFrame#SettingCard:hover {
    background-color: #333333;
    border: 1px solid #454545;
}
QLabel#CardTitle {
    font-size: 14px;
    font-weight: 600;
    color: #f0f0f0;
    background: transparent;
}
QLabel#CardDesc {
    font-size: 12px;
    color: #a0a0a0;
    background: transparent;
}
QLabel#CardIcon { background: transparent; }

QPushButton {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    padding: 6px 14px;
    color: #e8e8e8;
}
QPushButton:hover { background-color: #3a3a3a; }
QPushButton:pressed { background-color: #454545; }
QPushButton:disabled { color: #666666; background-color: #252525; }

QLineEdit, QComboBox, QSpinBox {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    border-radius: 6px;
    padding: 4px 8px;
    color: #e8e8e8;
}
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    border: 1px solid #3d3d3d;
    selection-background-color: #0067c0;
    color: #e8e8e8;
}

QCheckBox {
    spacing: 8px;
    color: #e8e8e8;
    background: transparent;
}
QCheckBox::indicator {
    width: 18px; height: 18px;
    border-radius: 4px;
    border: 1px solid #555555;
    background-color: #2d2d2d;
}
QCheckBox::indicator:checked {
    background-color: #0067c0;
    border: 1px solid #0067c0;
}

QSlider::groove:horizontal {
    height: 4px;
    background: #3d3d3d;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #4aa3ff;
    width: 16px; height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}

QListWidget {
    background-color: #2b2b2b;
    border: 1px solid #3d3d3d;
    border-radius: 8px;
    padding: 4px;
}
QListWidget::item {
    padding: 8px 10px;
    border-radius: 4px;
}
QListWidget::item:selected {
    background-color: #0067c0;
    color: #ffffff;
}
QListWidget::item:hover {
    background-color: #353535;
}
QListWidget::item:selected:hover {
    background-color: #005ba8;
    color: #ffffff;
}

QDialog { background-color: #202020; }

QScrollArea { border: none; background: transparent; }
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px;
}
QScrollBar::handle:vertical {
    background: #444444;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: #555555; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
"""