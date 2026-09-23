#include "config_parser.hpp"
#include "utils.hpp"

namespace alrm {

Config Config::load(const std::string& path) {
    Config config;
    std::string content = read_file(path);
    if (content.empty()) {
        log(LogLevel::WARN, "配置文件为空或不存在，使用默认配置: " + path);
        // 默认白名单
        config.whitelist = {"terminal", "spotify", "transmission", "clash", "v2ray"};
        return config;
    }
    
    std::istringstream stream(content);
    std::string line;
    while (std::getline(stream, line)) {
        // 跳过注释和空行
        if (line.empty() || line[0] == '#') continue;
        
        auto pos = line.find('=');
        if (pos == std::string::npos) continue;
        
        std::string key = line.substr(0, pos);
        std::string value = line.substr(pos + 1);
        
        // 去除空白
        key.erase(0, key.find_first_not_of(" \t"));
        key.erase(key.find_last_not_of(" \t") + 1);
        value.erase(0, value.find_first_not_of(" \t"));
        value.erase(value.find_last_not_of(" \t") + 1);
        
        // 解析配置项
        if (key == "SYSTEM_MODE") config.system_mode = value;
        else if (key == "AUTO_SLEEP_MODE") config.auto_sleep_mode = (value == "true");
        else if (key == "ENABLE_APP_NAP") config.enable_app_nap = (value == "true");
        else if (key == "SCAN_INTERVAL") config.scan_interval = std::stoi(value);
        else if (key == "FREEZE_TIMEOUT") config.freeze_timeout = std::stoi(value);
        else if (key == "CPU_THRESHOLD") config.cpu_threshold = std::stoi(value);
        else if (key == "WHITELIST_APPS") {
            config.whitelist = split(value, ',');
            for (auto& app : config.whitelist) {
                app.erase(0, app.find_first_not_of(" \t"));
                app.erase(app.find_last_not_of(" \t") + 1);
            }
        }
    }
    
    log(LogLevel::INFO, "配置加载完成: mode=" + config.system_mode 
        + ", app_nap=" + (config.enable_app_nap ? "on" : "off"));
    return config;
}

} // namespace alrm