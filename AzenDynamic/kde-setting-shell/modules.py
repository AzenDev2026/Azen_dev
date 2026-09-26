# modules.py
# 每个分类: (翻译 key, 图标名, 页面标识)
# 页面标识由 main.py 分发到对应的 Page 类

CATEGORIES = [
    ("system",      "computer",                  "page_system"),
    ("appearance",  "preferences-desktop-theme", "page_appearance"),
    ("keyboard",    "input-keyboard",            "page_keyboard"),
    ("mouse",       "input-mouse",               "page_mouse"),
    ("touchscreen", "input-tablet",              "page_touchscreen"),
    ("display",     "video-display",             "page_display"),
    ("network",     "network-wireless",          "page_network"),
    ("users",       "user-identity",             "page_users"),
    ("update",      "system-software-update",    "page_update"),
]

# 每个分类内，“打开原生设置”按钮对应的 KCM 模块名
NATIVE_KCM = {
    "page_system":      "kcm_kded",
    "page_appearance":  "kcm_lookandfeel",
    "page_keyboard":    "kcm_keyboard",
    "page_mouse":       "kcm_mouse",
    "page_touchscreen": "kcm_kwintouchscreen",
    "page_display":     "kcm_kscreen",
    "page_network":     "kcm_networkmanagement",
    "page_users":       "kcm_users",
    "page_update":      "kcm_updates",
}