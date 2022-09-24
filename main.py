from machine import I2C
from core.modem import Modem
from qwiic_keypad import QwiicKeypad

import ssd1306
from time import sleep

i2c = I2C()
myKeypad = QwiicKeypad(i2c)
display = ssd1306.SSD1306_I2C(128, 32, i2c)

def update_buffer(buffer, new_str):
    if new_str in ["*", "#", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        buffer += new_str
        if len(buffer) > 4:
            buffer = buffer[1:]
    return buffer
    
def clear_screen():
    display.fill(0)
    display.fill_rect(0, 0, 127, 32, 1)
    display.fill_rect(2, 2, 123, 28, 0)
    display.text(f"sixfab | ", 10, 12, 1)

if __name__ == "__main__":
    if not myKeypad.is_connected():
        raise Exception("The Qwiic Keypad device isn't connected to the system. Please check your connection")
    
    button = 0
    buffer = ""
    while True:
        
        myKeypad.update_fifo()  
        button = myKeypad.get_button()

        if button == -1:
            print("No keypad detected")
            time.sleep(1)

        elif button != 0:
            # Get the character version of this char
            clear_screen()
            charButton = chr(int.from_bytes(button, "little"))
            buffer = update_buffer(buffer, charButton)
            display.text(f"{buffer}", 82, 11, 1)
            display.show()

        sleep(0.20)

