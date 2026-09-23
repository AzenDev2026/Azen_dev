#include "lid_monitor.h"
#include "logger.h"
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <dirent.h>
#include <linux/input.h>

#define MODULE "lid"

static int lid_fd = -1;
static lid_state_t last_state = LID_UNKNOWN;

// 查找合盖开关的 input 设备
static int find_lid_input_device(void) {
    DIR *dir = opendir("/dev/input");
    if (!dir) return -1;
    
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strncmp(entry->d_name, "event", 5) != 0) continue;
        
        char path[256];
        snprintf(path, sizeof(path), "/dev/input/%s", entry->d_name);
        
        int fd = open(path, O_RDONLY | O_NONBLOCK);
        if (fd < 0) continue;
        
        // 检查设备是否支持 SW_LID
        unsigned long evbit = 0;
        if (ioctl(fd, EVIOCGBIT(0, sizeof(evbit)), &evbit) >= 0) {
            if (evbit & (1 << EV_SW)) {
                unsigned long swbit = 0;
                if (ioctl(fd, EVIOCGBIT(EV_SW, sizeof(swbit)), &swbit) >= 0) {
                    if (swbit & (1 << SW_LID)) {
                        LOG_INFO(MODULE, "找到合盖设备: %s", path);
                        closedir(dir);
                        return fd;
                    }
                }
            }
        }
        close(fd);
    }
    
    closedir(dir);
    return -1;
}

int lid_monitor_init(void) {
    lid_fd = find_lid_input_device();
    if (lid_fd < 0) {
        LOG_WARN(MODULE, "未找到合盖开关设备（可能不支持）");
        return -1;
    }
    
    // 读取初始状态
    last_state = lid_get_state();
    LOG_INFO(MODULE, "初始合盖状态: %s",
             last_state == LID_CLOSED ? "关闭" : "打开");
    
    return lid_fd;
}

lid_state_t lid_get_state(void) {
    // 优先从 /proc/acpi 读取
    const char *paths[] = {
        "/proc/acpi/button/lid/LID/state",
        "/proc/acpi/button/lid/LID0/state",
        NULL
    };
    
    for (int i = 0; paths[i]; i++) {
        FILE *fp = fopen(paths[i], "r");
        if (!fp) continue;
        
        char buf[64];
        if (fgets(buf, sizeof(buf), fp)) {
            fclose(fp);
            if (strstr(buf, "closed")) return LID_CLOSED;
            if (strstr(buf, "open")) return LID_OPEN;
        }
        fclose(fp);
    }
    
    return LID_UNKNOWN;
}

int lid_get_fd(void) {
    return lid_fd;
}

void lid_handle_event(void) {
    struct input_event ev;
    ssize_t n = read(lid_fd, &ev, sizeof(ev));
    
    if (n != sizeof(ev)) return;
    
    // 只处理 SW_LID 事件
    if (ev.type == EV_SW && ev.code == SW_LID) {
        lid_state_t new_state = ev.value ? LID_CLOSED : LID_OPEN;
        
        if (new_state != last_state) {
            LOG_INFO(MODULE, "合盖状态变化: %s",
                     new_state == LID_CLOSED ? "关闭" : "打开");
            last_state = new_state;
        }
    }
}

void lid_monitor_cleanup(void) {
    if (lid_fd >= 0) {
        close(lid_fd);
        lid_fd = -1;
    }
}