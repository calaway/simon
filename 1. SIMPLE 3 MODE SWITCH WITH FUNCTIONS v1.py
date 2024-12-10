"""
First attempt at combining all button and sound code
"""

import board
import digitalio
import neopixel
import keypad
import adafruit_rfm9x
import time
import audiocore
import audiopwmio

# Set up NeoPixel.
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.5

# Set up SIMON input buttons (USE KEYPAD module instead of direct pullup stuff)
# it debounces and sends as one key press. We set to false b/c pin goes low when pressed
# Set PULL to true b/c we dont have external resistor, so pin held high when not pressed
RedButton = keypad.Keys((board.TX,), value_when_pressed=False, pull=True)
YellowButton = keypad.Keys((board.RX,), value_when_pressed=False, pull=True)
GreenButton = keypad.Keys((board.D25,), value_when_pressed=False, pull=True)
BlueButton = keypad.Keys((board.D24,), value_when_pressed=False, pull=True)

# Add a button for mode switching
ModeButton = keypad.Keys((board.D13,), value_when_pressed=False, pull=True)

# Check if the ModeButton is pressed right after initialization
# I don't know why but this ensures it starts in mode 1
# without this it goes to mode 2 immediately? WEIRD
if ModeButton.events.get().pressed:
    print("ModeButton is pressed immediately after initialization")

# Define the modes
modes = ["ControllerMode", "LightsMode", "SoundMode"]
current_mode = 0  # This will start the program in ControllerMode
print(f"Starting in {modes[current_mode]}")

# Define a function for each mode
def ControllerMode():
    # THIS IS STANDARD CONTROLLER MODE
    # Check for button presses. If pressed, send a packet, set NeoPixel Color,
    # turn on the SIMON LED, Play a sound.
    # When released, turn off the NeoPixel and SIMON LED
    RedPress = RedButton.events.get()
    YellowPress = YellowButton.events.get()
    GreenPress = GreenButton.events.get()
    BluePress = BlueButton.events.get()
    if RedPress:
        if RedPress.pressed:
            rfm95.send(bytes("R", "UTF-8"))
            pixel.fill((255, 0, 0))
            RedLED.value = True
            audio.play(meowWav)
            print("RED!")
        if RedPress.released:
            pixel.fill((0, 0, 0))
            RedLED.value = False
    elif YellowPress:
        if YellowPress.pressed:
            rfm95.send(bytes("Y", "UTF-8"))
            pixel.fill((255, 245, 0))
            YellowLED.value = True
            audio.play(barkWav)
            print("YELLOW!")
        if YellowPress.released:
            pixel.fill((0, 0, 0))
            YellowLED.value = False
    elif GreenPress:
        if GreenPress.pressed:
            rfm95.send(bytes("G", "UTF-8"))
            pixel.fill((0, 255, 0))
            GreenLED.value = True
            audio.play(fartWav)
            print("GREEN!")
        if GreenPress.released:
            pixel.fill((0, 0, 0))
            GreenLED.value = False
    elif BluePress:
        if BluePress.pressed:
            rfm95.send(bytes("B", "UTF-8"))
            pixel.fill((0, 0, 255))
            BlueLED.value = True
            audio.play(blipWav)
            print("BLUE!")
        if BluePress.released:
            pixel.fill((0, 0, 0))
            BlueLED.value = False

def LightsMode():
    # Add functionality for LightsMode
    # THIS IS STANDARD CONTROLLER MODE BUT NO SOUNDS
    # Check for button presses. If pressed, send a packet, set NeoPixel Color,
    # turn on the SIMON LED, Play a sound.
    # When released, turn off the NeoPixel and SIMON LED
    RedPress = RedButton.events.get()
    YellowPress = YellowButton.events.get()
    GreenPress = GreenButton.events.get()
    BluePress = BlueButton.events.get()
    if RedPress:
        if RedPress.pressed:
            rfm95.send(bytes("R", "UTF-8"))
            pixel.fill((255, 0, 0))
            RedLED.value = True
            print("RED!")
        if RedPress.released:
            pixel.fill((0, 0, 0))
            RedLED.value = False
    elif YellowPress:
        if YellowPress.pressed:
            rfm95.send(bytes("Y", "UTF-8"))
            pixel.fill((255, 245, 0))
            YellowLED.value = True
            print("YELLOW!")
        if YellowPress.released:
            pixel.fill((0, 0, 0))
            YellowLED.value = False
    elif GreenPress:
        if GreenPress.pressed:
            rfm95.send(bytes("G", "UTF-8"))
            pixel.fill((0, 255, 0))
            GreenLED.value = True
            print("GREEN!")
        if GreenPress.released:
            pixel.fill((0, 0, 0))
            GreenLED.value = False
    elif BluePress:
        if BluePress.pressed:
            rfm95.send(bytes("B", "UTF-8"))
            pixel.fill((0, 0, 255))
            BlueLED.value = True
            print("BLUE!")
        if BluePress.released:
            pixel.fill((0, 0, 0))
            BlueLED.value = False

def SoundMode():
    # Add functionality for SoundMode
    # THIS IS STANDARD CONTROLLER MODE BUT NO LIGHTS
    # Check for button presses. If pressed, send a packet, set NeoPixel Color,
    # turn on the SIMON LED, Play a sound.
    # When released, turn off the NeoPixel and SIMON LED
    RedPress = RedButton.events.get()
    YellowPress = YellowButton.events.get()
    GreenPress = GreenButton.events.get()
    BluePress = BlueButton.events.get()
    if RedPress:
        if RedPress.pressed:
            rfm95.send(bytes("R", "UTF-8"))
            pixel.fill((255, 0, 0))
            audio.play(meowWav)
            print("RED!")
        if RedPress.released:
            pixel.fill((0, 0, 0))
    elif YellowPress:
        if YellowPress.pressed:
            rfm95.send(bytes("Y", "UTF-8"))
            pixel.fill((255, 245, 0))
            audio.play(barkWav)
            print("YELLOW!")
        if YellowPress.released:
            pixel.fill((0, 0, 0))
    elif GreenPress:
        if GreenPress.pressed:
            rfm95.send(bytes("G", "UTF-8"))
            pixel.fill((0, 255, 0))
            audio.play(fartWav)
            print("GREEN!")
        if GreenPress.released:
            pixel.fill((0, 0, 0))
    elif BluePress:
        if BluePress.pressed:
            rfm95.send(bytes("B", "UTF-8"))
            pixel.fill((0, 0, 255))
            audio.play(blipWav)
            print("BLUE!")
        if BluePress.released:
            pixel.fill((0, 0, 0))

# Setup up LED output pins
RedLED = digitalio.DigitalInOut(board.D5)
RedLED.direction = digitalio.Direction.OUTPUT
YellowLED = digitalio.DigitalInOut(board.D6)
YellowLED.direction = digitalio.Direction.OUTPUT
GreenLED = digitalio.DigitalInOut(board.D9)
GreenLED.direction = digitalio.Direction.OUTPUT
BlueLED = digitalio.DigitalInOut(board.D10)
BlueLED.direction = digitalio.Direction.OUTPUT

# Setup Sounds
meow = open("meow1.wav", "rb")
bark = open("bark1.wav", "rb")
fart = open("fart1.wav", "rb")
blip = open("blip.wav", "rb")
meowWav = audiocore.WaveFile(meow)
barkWav = audiocore.WaveFile(bark)
fartWav = audiocore.WaveFile(fart)
blipWav = audiocore.WaveFile(blip)
audio = audiopwmio.PWMAudioOut(board.A0)

# Define radio frequency in MHz. Must match your
# module. Can be a value like 915.0, 433.0, etc.
RADIO_FREQ_MHZ = 915.0

# Define Chip Select and Reset pins for the radio module.
CS = digitalio.DigitalInOut(board.RFM_CS)
RESET = digitalio.DigitalInOut(board.RFM_RST)

# Initialise RFM95 radio
rfm95 = adafruit_rfm9x.RFM9x(board.SPI(), CS, RESET, RADIO_FREQ_MHZ)

while True:
    # Check if the mode button is pressed
    ModePress = ModeButton.events.get()
    if ModePress and ModePress.pressed:
        # Switch to the next mode
        current_mode = (current_mode + 1) % len(modes)
        print(f"Switched to {modes[current_mode]}")

    # Run the function for the current mode
    if modes[current_mode] == "ControllerMode":
        ControllerMode()
    elif modes[current_mode] == "LightsMode":
        LightsMode()
    elif modes[current_mode] == "SoundMode":
        SoundMode()
