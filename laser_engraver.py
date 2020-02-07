import sys
import serial
import serial.tools.list_ports
import time
from keyboard import Keyboard

class LaserEngraver:
    def __init__(self, com=-1, debug=False):
        self.scale = 1
        self.laser_state = False
        self.debug_mode = debug
        self.debug_log = []

        if not debug:
            port_list = list(serial.tools.list_ports.comports())
            if len(port_list) == 0:
                sys.exit("No COM port connected!")
            com_index = 0 if com < 0 else com
            if com_index > len(port_list):
                sys.exit("COM port #{} does not exist!".format(com_index))
        
            self.serial = serial.Serial(port_list[com_index].device, 115200)
            print("Connected to port {}".format(self.serial.name))
            self.__wait_init__()
        else:
            print("Starting laser engraver in debug mode")
            print("All command will only be written in debug file")
            print("No serial communication is transmitted")

    def __read_serial__(self):
        if self.debug_mode:
            return None

        return self.serial.readline()

    def __write_serial__(self, command):
        message = "{}\r\n".format(command)
        if self.debug_mode:
            self.debug_log.append(message)
        else:
            self.serial.write(message.encode())

    def __wait_init__(self):
        self.__log__(self.__read_serial__())
        self.__log__(self.__read_serial__())
        self.__log__(self.__read_serial__())

    def __log__(self, byte_message):
        if byte_message == None:
            return

        message = byte_message.decode().strip()
        if message:
            print("SERIAL | {}".format(message))

    def __verify_response__(self, response_number=1):
        if self.debug_mode:
            return

        for _ in range(0, response_number):
            response = self.__read_serial__().strip().decode()
            if response != "ok":
                sys.exit("Serial error: {}".format(response))
            
    def unlock(self):
        self.__write_serial__("$X")
        self.__log__(self.__read_serial__())
        self.__verify_response__(2)

    def set_scale(self, scale):
        self.scale = scale

    def set_unit_mode(self, mode):
        if mode == "MILLIMETERS":
            self.__write_serial__("G21")
        elif mode == "INCHES":
            self.__write_serial__("G20")
        self.__verify_response__(2)

    def set_position_mode(self, mode):
        if mode == "ABSOLUTE":
            self.__write_serial__("G90")
        elif mode == "RELATIVE":
            self.__write_serial__("G91")
        self.__verify_response__(2)

    def set_laser(self, state):
        self.laser_state = state
        if state:
            self.__write_serial__("M3")
            self.__verify_response__(2)
        else:
            self.__write_serial__("M5")
            self.__verify_response__(2)
            if not self.debug_mode:
                time.sleep(0.3)

    def move(self, x, y, fast=False):
        movement_type = 0 if fast else 1
        command = "G{} X{:.2f} Y{:.2f}".format(movement_type, float(x) * self.scale, float(y) * self.scale)
        self.__write_serial__(command)
        self.__verify_response__(2)

    def toggle_laser(self):
        self.set_laser(not self.laser_state)

    def save_current_position(self):
        self.__write_serial__("G92 X0 Y0")
        self.__verify_response__(2)

    def calibrate(self):
        self.unlock()
        self.set_unit_mode("MILLIMETERS")
        self.set_position_mode("RELATIVE")
        
        print("Starting calibration...")
        print("Use key z|q|s|d to move up|left|down|right")
        print("Use key l to toggle laser")
        print("Use key w to quit")

        keyboard = Keyboard()
        keyboard.bind(ord("z"), lambda: self.move(0, -1))
        keyboard.bind(ord("s"), lambda: self.move(0, 1))
        keyboard.bind(ord("d"), lambda: self.move(-1, 0))
        keyboard.bind(ord("q"), lambda: self.move(1, 0))
        keyboard.bind(ord("l"), lambda: self.toggle_laser())
        keyboard.run(ord("w"))
        
        self.save_current_position()
        print("Current position saved as reference.")

    def save_debug_logs(self, path):
        with open(path, "w+") as filehandle:
            for line in self.debug_log:
                filehandle.write(line)