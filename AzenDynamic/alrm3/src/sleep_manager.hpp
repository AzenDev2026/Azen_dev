#ifndef ALRM_SLEEP_MANAGER_HPP
#define ALRM_SLEEP_MANAGER_HPP

#include "config_parser.hpp"
#include <string>

namespace alrm {

class SleepManager {
public:
    SleepManager(const Config& config);
    
    // 切换到深度睡眠模式
    bool enable_deep_sleep();
    
    // 切换到浅睡眠模式
    bool enable_s2idle();
    
    // 根据配置自动选择
    bool apply_config();
    
    // 获取当前睡眠模式
    std::string get_current_mode();
    
    // 检查硬件支持
    std::vector<std::string> get_supported_modes();
    
private:
    Config config_;
    bool switch_mode(const std::string& mode);
};

} // namespace alrm

#endif