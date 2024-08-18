import RPi.GPIO as gpio

class AlarmHid:
    def __init__(self, enable_gpio, disable_gpio, reset_gpio, heartbeat_gpio, run_gpio, alarm_gpio):
        gpio.setmode(gpio.BCM)
        self.enable_gpio = enable_gpio
        gpio.setup(enable_gpio, gpio.IN, pull_up_down=gpio.PUD_UP)
        self.disable_gpio = disable_gpio
        gpio.setup(disable_gpio, gpio.IN, pull_up_down=gpio.PUD_UP)
        self.reset_gpio = reset_gpio
        gpio.setup(reset_gpio, gpio.IN, pull_up_down=gpio.PUD_UP)
        self.heartbeat_gpio = heartbeat_gpio
        gpio.setup(heartbeat_gpio, gpio.OUT)
        self.run_gpio = run_gpio
        gpio.setup(run_gpio, gpio.OUT)
        self.alarm_gpio = alarm_gpio
        gpio.setup(alarm_gpio, gpio.OUT)
        self.heartbeat_state = False
        self.alarm_enabled = True

    def reset_lights(self):
        gpio.output(self.heartbeat_gpio, gpio.LOW)
        gpio.output(self.run_gpio, gpio.LOW)
        gpio.output(self.alarm_gpio, gpio.LOW)

    def read_input(self):
        if not gpio.input(self.enable_gpio):
            self.alarm_enabled = True
        elif not gpio.input(self.disable_gpio):
            self.alarm_enabled = False
        gpio.output(self.run_gpio, gpio.HIGH if self.alarm_enabled else gpio.LOW)

    def get_alarm_enabled(self):
        return self.alarm_enabled
    
    def get_reset_button(self):
        return not gpio.input(self.reset_gpio)

    def heartbeat(self):
        self.heartbeat_state = not self.heartbeat_state
        gpio.output(self.heartbeat_gpio, gpio.HIGH if self.heartbeat_state else gpio.LOW)

    def set_alarm(self):
        gpio.output(self.alarm_gpio, gpio.HIGH)

    def reset_alarm(self):
        gpio.output(self.alarm_gpio, gpio.LOW)
        





