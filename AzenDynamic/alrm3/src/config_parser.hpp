#ifndef ALRM_CONFIG_PARSER_HPP
#define ALRM_CONFIG_PARSER_HPP

#include <string>
#include <vector>
#include <map>

namespace alrm {

struct Config {
    std::string system_mode = "balanced";
    bool auto_sleep_mode = true;
    bool enable_app_nap = true;
    int scan_interval = 5;           // 秒
    int freeze_timeout = 3600;       // 秒
    std::vector<std::string> whitelist;
    int cpu_threshold = 5;           // CPU 使用率阈值 (%)
    
    // 解析配置文件
    static Config load(const std::string& path);
    
    // 检查是否处于性能模式
    bool is_performance_mode() const { return system_mode == "performance"; }
    bool is_energy_saver() const { return system_mode == "energy-saver"; }
};

} // namespace alrm

#endif