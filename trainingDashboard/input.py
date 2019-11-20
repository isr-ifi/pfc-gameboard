import serial
import serial.tools.list_ports


# Enables user input for an area name after a card has been played
def request_area_name(self):
    self.ids.area_name.disabled = False
    self.ids.area_name.text = ''
    self.ids.submit_name.disabled = False


# Saves the area name given by the user (if length is within a valid range)
# and sends "TRAIN_OK" message to request new training data
def submit_area_name(self, name):
    if 0 < len(name) < 20:
        self.ids.area_name.disabled = True
        self.ids.area_name.text = ''
        self.ids.submit_name.disabled = True

        # Save name to temp data
        self.tempData[0] = name

        # Confirm received training data
        self.ser.write(b'TRAIN_OK')
        self.save_training_data(self.tempData)
        # Enable upload after we have at least one row of data
        self.ids.upload.disabled = False
    else:
        self.update_log('Error: Name too long')
