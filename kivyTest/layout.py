import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
import sys
import glob
import serial
import serial.tools.list_ports


Window.clearcolor = (0.8, 0.8, 0.8, 1)


# Get a list of available serial ports TODO check on windows
def serial_ports():
    res = []
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist: # TODO: possibly filter out NA's for second field here (check with print(element)
        connected.append(element.device)
        name = str(element.device).replace('/dev/cu.', '')
        res.append(name)
    return res




class MyGrid(Widget):

    connected = False
    ports = ['None']
    selectedPort = None

    def btn(self):
        print("Pressed")

    # Update the list of available ports
    def update_ports(self):
        print('updating ports...')
        self.ports = serial_ports()
        self.ids.port_dropdown.values = self.ports

    def start_finish_training(self):
        if self.saf.text == 'Start Training':
            self.saf.text = 'Finish Training'
            # Disable upload btn until finished
            self.ids.upload.disabled = True

        else:
            self.saf.text = 'Start Training'
            # Enable upload button after finishing training
            self.ids.upload.disabled = False

    def upload(self):
        if self.selectedPort is not None:
            print("upload to port " + str(self.selectedPort))
        else:
            print("can't upload")

    # Selects a given port to connect to
    def select_port(self, port):
        print("Port selected: " + str(port))
        self.selectedPort = port
        # enable start button
        self.ids.start_and_finish.disabled = False


# Main App definition
class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()