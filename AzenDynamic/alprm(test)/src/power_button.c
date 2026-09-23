#include "power_button.h"
#include "logger.h"
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <dirent.h>
#include <linux/input.h>

#define MODULE "power_button"

static int pb_fd = -1;

static int find_power_button_device(void) {
    DIR *dir = opendir("/dev/input");
    if (!dir) return -1;
    
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (strncmp(entry->d_name, "event", 5) != 0) continue;
        
        char path[256];
        snprintf(path, sizeof(path), "/dev/input/%s", entry->d_name);
        
        int fd = open(path, O_RDONLY | O_NONBLOCK);
        if (fd < 0) continue;
        
        // 检查是否支持 KEY_POWER
        unsigned long evbit = 0;
        if (ioctl(fd, EVIOCGBIT(0, sizeof(evbit)), &evbit) >= 0) {
            if (evbit & (1 << EV_KEY)) {
                unsigned long keybit = 0;
                if (ioctl(fd, EVIOCGBIT(EV_KEY, sizeof(keybit)), &keybit) >= 0) {
                    if (keybit & (1 << KEY_POWER)) {
                        LOG_INFO(MODULE, "找到电源键设备: %s", path);
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

int power_button_init(void) {
    pb_fd = find_power_button_device();
    if (pb_fd < 0) {
        LOG_WARN(MODULE, "未找到电源键设备");
        return -1;
    }
    LOG_INFO(MODULE, "电源键监听已启动");
    return pb_fd;
}

int power_button_get_fd(void) {
    return pb_fd;
}

void power_button_handle_event(void) {
    struct input_event ev;
    ssize_t n = read(pb_fd, &ev, sizeof(ev));
    
    if (n != sizeof(ev)) return;
    
    if (ev.type == EV_KEY && ev.code == KEY_POWER) {
        if (ev.value == 1) {
            LOG_INFO(MODULE, "电源键按下");
        } else if (ev.value == 0) {
            LOG_INFO(MODULE, "电源键释放");
        }
    }
}

void power_button_cleanup(void) {
    if (pb_fd >= 0) {
        close(pb_fd);
        pb_fd = -1;
    }
}