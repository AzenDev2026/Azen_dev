#ifndef ALPRM_LOGGER_H
#define ALPRM_LOGGER_H

#include <time.h>

#define ALPRM_LOG_DIR  "/etc/ALPRM_log"
#define ALPRM_LOG_FILE "/etc/ALPRM_log/events.log"

// 日志级别
typedef enum {
    LOG_INFO,
    LOG_WARN,
    LOG_ERROR,
    LOG_DEBUG
} log_level_t;

// 初始化日志系统（创建目录）
int logger_init(void);

// 写日志
void alprm_log(log_level_t level, const char *module, const char *fmt, ...);

// 便捷宏
#define LOG_INFO(mod, ...)  alprm_log(LOG_INFO,  mod, __VA_ARGS__)
#define LOG_WARN(mod, ...)  alprm_log(LOG_WARN,  mod, __VA_ARGS__)
#define LOG_ERROR(mod, ...) alprm_log(LOG_ERROR, mod, __VA_ARGS__)
#define LOG_DEBUG(mod, ...) alprm_log(LOG_DEBUG, mod, __VA_ARGS__)

#endif