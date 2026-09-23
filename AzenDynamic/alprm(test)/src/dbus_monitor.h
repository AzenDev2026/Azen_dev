#ifndef ALPRM_DBUS_MONITOR_H
#define ALPRM_DBUS_MONITOR_H

int dbus_monitor_init(void);
int dbus_monitor_get_fd(void);
void dbus_monitor_handle_event(void);
void dbus_monitor_cleanup(void);

#endif