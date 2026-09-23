#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/epoll.h>
#include <errno.h>

#include "logger.h"
#include "lid_monitor.h"
#include "power_button.h"
#include "dbus_monitor.h"

#define MODULE "main"
#define MAX_EVENTS 16

static volatile int running = 1;

static void signal_handler(int sig) {
    if (sig == SIGINT || sig == SIGTERM) {
        LOG_INFO(MODULE, "收到退出信号，正在清理...");
        running = 0;
    }
}

static void print_banner(void) {
    printf("\n");
    printf("================================================\n");
    printf("  ALPRM Monitor v0.1\n");
    printf("  Azen Laptop Power Resources Management\n");
    printf("  纯监听模式 - 不干预系统睡眠行为\n");
    printf("================================================\n");
    printf("  日志文件: %s\n", ALPRM_LOG_FILE);
    printf("  按 Ctrl+C 退出\n");
    printf("================================================\n\n");
}

int main(int argc, char *argv[]) {
    // 注册信号
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);
    
    print_banner();
    
    // 初始化日志
    if (logger_init() != 0) {
        fprintf(stderr, "日志初始化失败，退出\n");
        return 1;
    }
    
    LOG_INFO(MODULE, "================ ALPRM Monitor 启动 ================");
    
    // 创建 epoll
    int epfd = epoll_create1(0);
    if (epfd < 0) {
        LOG_ERROR(MODULE, "epoll_create1 失败: %s", strerror(errno));
        return 1;
    }
    
    // 初始化各模块
    int lid_fd = lid_monitor_init();
    int pb_fd = power_button_init();
    int dbus_ok = (dbus_monitor_init() == 0);
    int dbus_fd = dbus_monitor_get_fd();
    
    // 注册到 epoll
    struct epoll_event ev;
    
    if (lid_fd >= 0) {
        ev.events = EPOLLIN;
        ev.data.fd = lid_fd;
        epoll_ctl(epfd, EPOLL_CTL_ADD, lid_fd, &ev);
    }
    
    if (pb_fd >= 0) {
        ev.events = EPOLLIN;
        ev.data.fd = pb_fd;
        epoll_ctl(epfd, EPOLL_CTL_ADD, pb_fd, &ev);
    }
    
    if (dbus_ok && dbus_fd >= 0) {
        ev.events = EPOLLIN;
        ev.data.fd = dbus_fd;
        epoll_ctl(epfd, EPOLL_CTL_ADD, dbus_fd, &ev);
    }
    
    LOG_INFO(MODULE, "所有监听模块已启动，等待事件...");
    
    // 主循环
    struct epoll_event events[MAX_EVENTS];
    
    while (running) {
        int n = epoll_wait(epfd, events, MAX_EVENTS, 1000);
        
        if (n < 0) {
            if (errno == EINTR) continue;
            LOG_ERROR(MODULE, "epoll_wait 失败: %s", strerror(errno));
            break;
        }
        
        for (int i = 0; i < n; i++) {
            int fd = events[i].data.fd;
            
            if (fd == lid_fd) {
                lid_handle_event();
            } else if (fd == pb_fd) {
                power_button_handle_event();
            } else if (dbus_ok && fd == dbus_fd) {
                dbus_monitor_handle_event();
            }
        }
    }
    
    // 清理
    LOG_INFO(MODULE, "正在关闭监听模块...");
    
    lid_monitor_cleanup();
    power_button_cleanup();
    dbus_monitor_cleanup();
    close(epfd);
    
    LOG_INFO(MODULE, "================ ALPRM Monitor 已退出 ================");
    
    return 0;
}