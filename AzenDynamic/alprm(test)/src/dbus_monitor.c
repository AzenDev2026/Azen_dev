#include "dbus_monitor.h"
#include "logger.h"
#include <systemd/sd-bus.h>
#include <stdio.h>

#define MODULE "dbus"

static sd_bus *bus = NULL;
static sd_bus_slot *slot = NULL;

// PrepareForSleep 信号处理
static int on_prepare_for_sleep(sd_bus_message *m, void *userdata,
                                 sd_bus_error *ret_error) {
    int sleeping;
    int r = sd_bus_message_read(m, "b", &sleeping);
    if (r < 0) {
        LOG_ERROR(MODULE, "解析 PrepareForSleep 失败: %s", strerror(-r));
        return 0;
    }
    
    if (sleeping) {
        LOG_INFO(MODULE, "系统准备进入睡眠 (PrepareForSleep=true)");
    } else {
        LOG_INFO(MODULE, "系统正在从睡眠唤醒 (PrepareForSleep=false)");
    }
    
    return 0;
}

int dbus_monitor_init(void) {
    int r;
    
    // 连接系统总线
    r = sd_bus_open_system(&bus);
    if (r < 0) {
        LOG_ERROR(MODULE, "无法连接系统 D-Bus: %s", strerror(-r));
        return -1;
    }
    
    // 订阅 PrepareForSleep 信号
    r = sd_bus_match_signal(
        bus, &slot,
        "org.freedesktop.login1",           // sender
        "/org/freedesktop/login1",          // path
        "org.freedesktop.login1.Manager",   // interface
        "PrepareForSleep",                   // member
        on_prepare_for_sleep,               // callback
        NULL
    );
    
    if (r < 0) {
        LOG_ERROR(MODULE, "订阅 PrepareForSleep 失败: %s", strerror(-r));
        sd_bus_unref(bus);
        bus = NULL;
        return -1;
    }
    
    LOG_INFO(MODULE, "D-Bus 睡眠信号监听已启动");
    return 0;
}

int dbus_monitor_get_fd(void) {
    if (!bus) return -1;
    return sd_bus_get_fd(bus);
}

void dbus_monitor_handle_event(void) {
    if (!bus) return;
    
    int r;
    // 处理所有待处理消息
    while ((r = sd_bus_process(bus, NULL)) > 0) {
        // 继续处理
    }
    
    if (r < 0) {
        LOG_ERROR(MODULE, "D-Bus 处理失败: %s", strerror(-r));
    }
}

void dbus_monitor_cleanup(void) {
    if (slot) {
        sd_bus_slot_unref(slot);
        slot = NULL;
    }
    if (bus) {
        sd_bus_unref(bus);
        bus = NULL;
    }
}