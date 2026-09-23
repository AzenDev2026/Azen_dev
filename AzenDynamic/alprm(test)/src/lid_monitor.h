#ifndef ALPRM_LID_MONITOR_H
#define ALPRM_LID_MONITOR_H

// 合盖状态
typedef enum {
    LID_UNKNOWN = -1,
    LID_OPEN = 0,
    LID_CLOSED = 1
} lid_state_t;

// 初始化（返回文件描述符，失败返回 -1）
int lid_monitor_init(void);

// 读取当前合盖状态
lid_state_t lid_get_state(void);

// 获取监听用的文件描述符（用于 epoll）
int lid_get_fd(void);

// 处理事件
void lid_handle_event(void);

// 清理
void lid_monitor_cleanup(void);

#endif