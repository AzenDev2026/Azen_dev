#ifndef ALPRM_POWER_BUTTON_H
#define ALPRM_POWER_BUTTON_H

int power_button_init(void);
int power_button_get_fd(void);
void power_button_handle_event(void);
void power_button_cleanup(void);

#endif