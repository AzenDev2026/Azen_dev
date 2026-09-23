#include "logger.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>

static const char *level_str[] = {"INFO", "WARN", "ERROR", "DEBUG"};

int logger_init(void) {
    struct stat st = {0};
    
    // 创建日志目录
    if (stat(ALPRM_LOG_DIR, &st) == -1) {
        if (mkdir(ALPRM_LOG_DIR, 0755) != 0) {
            fprintf(stderr, "无法创建日志目录 %s: %s\n",
                    ALPRM_LOG_DIR, strerror(errno));
            return -1;
        }
    }
    
    // 测试日志文件是否可写
    FILE *fp = fopen(ALPRM_LOG_FILE, "a");
    if (!fp) {
        fprintf(stderr, "无法打开日志文件 %s: %s\n",
                ALPRM_LOG_FILE, strerror(errno));
        return -1;
    }
    fclose(fp);
    
    return 0;
}

void alprm_log(log_level_t level, const char *module, const char *fmt, ...) {
    FILE *fp = fopen(ALPRM_LOG_FILE, "a");
    if (!fp) return;
    
    // 时间戳
    time_t now = time(NULL);
    struct tm *tm_info = localtime(&now);
    char time_buf[32];
    strftime(time_buf, sizeof(time_buf), "%Y-%m-%d %H:%M:%S", tm_info);
    
    // 前缀
    fprintf(fp, "[%s] [%s] [%s] ",
            time_buf, level_str[level], module);
    
    // 用户消息
    va_list args;
    va_start(args, fmt);
    vfprintf(fp, fmt, args);
    va_end(args);
    
    fprintf(fp, "\n");
    fclose(fp);
    
    // 同时输出到 stderr（方便调试）
    fprintf(stderr, "[%s] [%s] [%s] ",
            time_buf, level_str[level], module);
    va_start(args, fmt);
    vfprintf(stderr, fmt, args);
    va_end(args);
    fprintf(stderr, "\n");
}