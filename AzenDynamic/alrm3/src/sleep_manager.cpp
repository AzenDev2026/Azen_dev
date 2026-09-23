#include "sleep_manager.hpp"
#include "utils.hpp"
#include <algorithm>

namespace alrm {

SleepManager::SleepManager(const Config& config) : config_(config) {}

std::vector<std::string> SleepManager::get_supported_modes() {
    std::string content = read_file("/sys/power/mem_sleep");
    if (content.empty()) return {};
    
    // 解析 [s2idle] deep 格式
    std::vector<std::string> modes;
    std::string current;
    bool in_bracket = false;
    
    for (char c : content) {
        if (c == '[') {
            in_bracket = true;
            current.clear();
        } else if (c == ']') {
            in_bracket = false;
            modes.push_back(current);
        } else if (in_bracket) {
            current += c;
        } else if (c != ' ' && c != '\n') {
            // 非括号内的模式名
        }
    }
    
    // 简化处理：直接分割
    auto parts = split(content, ' ');
    for (auto& part : parts) {
        part.erase(std::remove(part.begin(), part.end(), '['), part.end());
        part.erase(std::remove(part.begin(), part.end(), ']'), part.end());
        part.erase(std::remove(part.begin(), part.end(), '\n'), part.end());
        if (!part.empty()) {
            modes.push_back(part);
        }
    }
    
    return modes;
}

std::string SleepManager::get_current_mode() {
    std::string content = read_file("/sys/power/mem_sleep");
    auto start = content.find('[');
    auto end = content.find(']');
    if (start != std::string::npos && end != std::string::npos) {
        return content.substr(start + 1, end - start - 1);
    }
    return "unknown";
}

bool SleepManager::switch_mode(const std::string& mode) {
    auto supported = get_supported_modes();
    if (std::find(supported.begin(), supported.end(), mode) == supported.end()) {
        log(LogLevel::WARN, "模式 " + mode + " 不被硬件支持");
        return false;
    }
    
    if (get_current_mode() == mode) {
        log(LogLevel::DEBUG, "已经处于 " + mode + " 模式");
        return true;
    }
    
    if (write_file("/sys/power/mem_sleep", mode)) {
        log(LogLevel::INFO, "✅ 睡眠模式切换: " + mode);
        return true;
    }
    
    log(LogLevel::ERROR, "切换睡眠模式失败");
    return false;
}

bool SleepManager::enable_deep_sleep() {
    return switch_mode("deep");
}

bool SleepManager::enable_s2idle() {
    return switch_mode("s2idle");
}

bool SleepManager::apply_config() {
    if (config_.is_energy_saver()) {
        log(LogLevel::INFO, "⚡ 节能模式: 启用深度睡眠");
        return enable_deep_sleep();
    } else if (config_.is_performance_mode()) {
        log(LogLevel::INFO, "⚡ 性能模式: 启用浅睡眠");
        return enable_s2idle();
    } else {
        // 平衡模式：检查电源状态
        std::string bat_status = read_file("/sys/class/power_supply/BAT0/status");
        if (bat_status.find("Discharging") != std::string::npos) {
            log(LogLevel::INFO, "⚖️  电池供电，启用深度睡眠");
            return enable_deep_sleep();
        } else {
            log(LogLevel::INFO, "⚖️  外接电源，启用浅睡眠");
            return enable_s2idle();
        }
    }
}

} // namespace alrm