def init_controls(self):
    """Define keys and add listener"""
    self.controls = {
        'w': 'forward',
        's': 'backward',
        'a': 'left',
        'd': 'right',
        'Key.space': 'up',
        'Key.shift': 'down',
        'Key.shift_r': 'down',
        'q': 'counter_clockwise',
        'e': 'clockwise',
        'i': lambda speed: self.drone.flip_forward(),
        'k': lambda speed: self.drone.flip_back(),
        'j': lambda speed: self.drone.flip_left(),
        'l': lambda speed: self.drone.flip_right(),
        # arrow keys for fast turns and altitude adjustments
        'Key.left': lambda speed: self.drone.counter_clockwise(speed),
        'Key.right': lambda speed: self.drone.clockwise(speed),
        'Key.up': lambda speed: self.drone.up(speed),
        'Key.down': lambda speed: self.drone.down(speed),
        'Key.tab': lambda speed: self.drone.takeoff(),
        'Key.backspace': lambda speed: self.drone.land(),
        'p': lambda speed: self.palm_land(speed),
        't': lambda speed: self.toggle_tracking(speed),
        'r': lambda speed: self.toggle_recording(speed),
        'z': lambda speed: self.toggle_zoom(speed),
        'Key.enter': lambda speed: self.take_picture(speed)
    }
    self.key_listener = keyboard.Listener(on_press=self.on_press,
                                            on_release=self.on_release)
    self.key_listener.start()