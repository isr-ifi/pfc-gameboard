import kivy
from kivy.config import Config
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '750')
Config.set('graphics', 'minimum_width', '1000')
Config.set('graphics', 'minimum_height', '750')
from kivy.core.window import Window
#Window.size = (1000, 750)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import sys
import glob
import serial
import serial.tools.list_ports
import platform


Window.clearcolor = (0.8, 0.8, 0.8, 1)


class MyGrid(Widget):
    log = ''
    ser = serial.Serial(None)
    connected = False
    ports = ['No Devices Found']
    selectedPort = None
    selectedPort_Windows = None

    # Get a list of available serial ports TODO check on windows
    def serial_ports(self):
        names = []
        comlist = serial.tools.list_ports.comports()
        for element in comlist:
            # UNIX (Macos/Linux): filter device
            if platform.system() is not "Windows":
                # Filter out ports with no product description - add all that contain "GameBoard" (for Bluetooth ports)
                if element.product is not None or "GameBoard" in element.device:
                    name = str(element.device).replace('/dev/cu.', '').replace('/dev/tty.', '')
                    names.append(name)
            else:
                index = element.description.find('(')
                cut_string = element.description[:index-1]
                names.append(cut_string)
                self.selectedPort_Windows = element.device

        if len(names) == 0:
            names.append('No Devices Found')

        result = names
        return result

    # Update the list of available ports
    def update_ports(self):
        self.update_log('Getting device list...')
        self.ports = self.serial_ports()
        self.ids.port_dropdown.values = self.ports

        if self.ids.port_dropdown.values[0] == 'No Devices Found':
            self.ids.port_dropdown.text = 'No Devices Found'
            self.ids.port_dropdown.values = ''

    # Start or finish the training process
    def start_training(self):
        self.ids.reboot.disabled = False
        self.update_log('Started Training!')
        self.ids.instructions.text = '''1. Activate each area 
(in alphabetical order)

2. Do you have an Oracle? '''
        self.ids.oracle_yes.disabled = False
        self.ids.oracle_no.disabled = False
        self.ids.start_training.disabled = True

    def oracle_yes(self):
        self.ids.oracle_yes.disabled = True
        self.ids.oracle_no.disabled = True
        self.ids.instructions.text = 'Activate the Oracle and press "Upload to Board"'
        self.ids.upload.disabled = False
        self.update_log('Oracle incoming...')

    def oracle_no(self):
        self.ids.oracle_yes.disabled = True
        self.ids.oracle_no.disabled = True
        self.ids.instructions.text = 'Press "Upload to Board"'
        self.ids.upload.disabled = False
        self.update_log('No Oracle')

    # Upload new training data
    def upload(self):
        self.ids.reboot.disabled = True
        self.update_log('Upload starting...')
        self.ids.upload.disabled = True
        if self.selectedPort is not None:
            self.update_log("Connecting to port {}...".format(self.selectedPort))
            try:
                self.update_log('Connected to port\n{}, uploading...'.format(self.ser.name))
                self.ser.write(b'CHANGE_MODE=1')  # write data as bytes
                self.ids.upload.disabled = True
                # self.ser.close()  # close port TODO check need
            except OSError:
                self.update_log('Error occurred')  # TODO Error handling

        # TODO integrate into check if upload actually worked
        self.ids.instructions.text = '''All done! 
You can close the dashboard
and start playing'''

    def reboot(self):
        self.ids.start_training.disabled = False
        self.ids.upload.disabled = True
        self.ids.start_training.text = 'Start Training'
        self.ids.instructions.text = 'Press "Start Training"'
        self.update_log('Rebooting...')  # TODO disconnect as well
        # Send reboot command
        self.ser.write(b'RESTART_TRAINING')  # write data as bytes
        self.ids.reboot.disabled = True
        self.ids.oracle_yes.disabled = True
        self.ids.oracle_no.disabled = True

    # Toggle Log visibility
    def toggle_log(self, value):
        if not value:
            self.ids.log.height = 0
            self.ids.log.size_hint_y = None
            self.ids.log.text = ''
        else:
            self.ids.log.height = self.parent.height * 0.72
            self.ids.log.size_hint_y = None
            self.ids.log.text = 'Log:\n' + self.log

    # Selects a given port to connect to
    def select_port(self, port):

        if str(port) == 'No Devices Found':
            return

        try:
            self.update_log("Port selected: {}".format(port))
            self.selectedPort = port
            idx = self.ports.index(port)

            # Enable serial port (system dependent)
            if platform.system() is not "Windows":
                self.ser = serial.Serial('/dev/cu.' + str(self.selectedPort), 57600)  # open serial port
            else:
                self.ser = serial.Serial(str(self.selectedPort_Windows), 57600)  # open serial port

            # Enable start button
            self.ids.start_training.disabled = False
        except OSError:
            self.update_log('Error: Could not open port')
            self.toggle_log(True)

    # Update the integrated log
    def update_log(self, text):
        print(text)
        self.log += (text + '\n')

        # Update Log text only if visible
        if self.ids.chk.active:
            self.ids.log.text = 'Log:\n' + self.log


# Main App definition
class MyApp(App):
    title = "Game Board Training Dashboard"

    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
