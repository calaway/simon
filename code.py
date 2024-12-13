"""
Production readish kinda basic controller and Simon game code
Starts in Controller mode where when you press a button, the corresponding
LED lights up, a packet is sent to the traffic light, and a sound is played

Power button changes mode to SIMON game mode where the game is played,
but only on the traffic light. After startup sequence, the controller doesn't play a sound or light up
it is all done on the traffic light. Blue button is all traffic lights on.

MAAAYBE have another mode that uses other sounds or no sounds on the controller before going to simon mode
"""

import random
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
# meow = open("meow1.wav", "rb")
# bark = open("bark1.wav", "rb")
fart = open("fart1.wav", "rb")
# blip = open("blip.wav", "rb")
cont = open("controller.wav", "rb")
sim = open("simonMode.wav", "rb")
redSound = open("Red_252.wav", "rb")
yellowSound = open("Yellow_310.wav", "rb")
greenSound = open("Green_209.wav", "rb")
blueSound = open("Blue_415.wav", "rb")
loseSound = open("lose_42.wav", "rb")

# meowWav = audiocore.WaveFile(meow)
# barkWav = audiocore.WaveFile(bark)
fartWav = audiocore.WaveFile(fart)
# blipWav = audiocore.WaveFile(blip)
contWav = audiocore.WaveFile(cont)
simWav = audiocore.WaveFile(sim)
redWav = audiocore.WaveFile(redSound)
yellowWav = audiocore.WaveFile(yellowSound)
greenWav = audiocore.WaveFile(greenSound)
blueWav = audiocore.WaveFile(blueSound)
loseWav = audiocore.WaveFile(loseSound)

audio = audiopwmio.PWMAudioOut(board.A0)

# Define the buttons and LEDs in a list for easy access
buttons = [RedButton, YellowButton, GreenButton, BlueButton, ModeButton]
leds = [RedLED, YellowLED, GreenLED, BlueLED]
sounds = [redWav, yellowWav, greenWav, blueWav]
packets = ["R", "Y", "G", "B"]

# Define radio frequency in MHz. Must match your
# module. Can be a value like 915.0, 433.0, etc.
RADIO_FREQ_MHZ = 915.0

# Define Chip Select and Reset pins for the radio module.
CS = digitalio.DigitalInOut(board.RFM_CS)
RESET = digitalio.DigitalInOut(board.RFM_RST)

# Initialise RFM95 radio
rfm95 = adafruit_rfm9x.RFM9x(board.SPI(), CS, RESET, RADIO_FREQ_MHZ)

# Define the modes
modes = ["ControllerMode", "SimonGame"]
current_mode = 0  # This will start the program in ControllerMode mode
print(f"Starting in {modes[current_mode]}")

# Define a function for each mode
# THIS IS STANDARD CONTROLLER MODE
def ControllerMode():
    print("Entering controller mode")
    audio.play(contWav)
    while audio.playing:
        pass
    while True:
        # Check for button presses. If pressed, send a packet, set NeoPixel Color,
        # turn on the SIMON LED, Play a sound.
        # When released, turn off the NeoPixel and SIMON LED
        ModePress = ModeButton.events.get()
        RedPress = RedButton.events.get()
        YellowPress = YellowButton.events.get()
        GreenPress = GreenButton.events.get()
        BluePress = BlueButton.events.get()
        if ModePress and ModePress.pressed:
            # Play the simWav sound file when the mode button is pressed
            audio.play(simWav)
            while audio.playing:
                pass
            # pause for a fifth of a second
            time.sleep(0.2)
            rfm95.send(bytes("O", "UTF-8"))  # Send an off packet to turn off all LEDs before game starts
            break
        if RedPress:
            if RedPress.pressed:
                rfm95.send(bytes("R", "UTF-8"))
                pixel.fill((255, 0, 0))
                RedLED.value = True
                audio.play(redWav)
                print("RED!")
            if RedPress.released:
                pixel.fill((0, 0, 0))
                RedLED.value = False
        elif YellowPress:
            if YellowPress.pressed:
                rfm95.send(bytes("Y", "UTF-8"))
                pixel.fill((255, 245, 0))
                YellowLED.value = True
                audio.play(yellowWav)
                print("YELLOW!")
            if YellowPress.released:
                pixel.fill((0, 0, 0))
                YellowLED.value = False
        elif GreenPress:
            if GreenPress.pressed:
                rfm95.send(bytes("G", "UTF-8"))
                pixel.fill((0, 255, 0))
                GreenLED.value = True
                audio.play(greenWav)
                print("GREEN!")
            if GreenPress.released:
                pixel.fill((0, 0, 0))
                GreenLED.value = False
        elif BluePress:
            if BluePress.pressed:
                rfm95.send(bytes("B", "UTF-8"))
                pixel.fill((0, 0, 255))
                BlueLED.value = True
                audio.play(blueWav)
                print("BLUE!")
            if BluePress.released:
                pixel.fill((0, 0, 0))
                BlueLED.value = False


# THIS IS SIMON GAME MODE
def SimonGame():
    print("Entering Simon game mode")
    # Initialize the delay time and round counter
    playback_delay_time = 0.5
    player_delay_time = 0.3
    round_counter = 0

    exit_game = False
    while True:  # Outer loop to restart the game
         # play all 4 colors, their sound, and light the traffic light to start the game
        YellowLED.value = True
        audio.play(yellowWav)
        rfm95.send(bytes("Y", "UTF-8"))
        time.sleep(0.1)
        YellowLED.value = False
        rfm95.send(bytes("O", "UTF-8"))
        time.sleep(0.1)
        GreenLED.value = True
        audio.play(greenWav)
        rfm95.send(bytes("G", "UTF-8"))
        time.sleep(0.1)
        GreenLED.value = False
        rfm95.send(bytes("O", "UTF-8"))
        time.sleep(0.1)
        RedLED.value = True
        audio.play(redWav)
        rfm95.send(bytes("R", "UTF-8"))
        time.sleep(0.1)
        RedLED.value = False
        rfm95.send(bytes("O", "UTF-8"))
        time.sleep(0.1)
        BlueLED.value = True
        audio.play(blueWav)
        rfm95.send(bytes("B", "UTF-8"))
        time.sleep(0.1)
        BlueLED.value = False
        rfm95.send(bytes("O", "UTF-8"))
        time.sleep(1.5)

        # Game sequence
        game_sequence = []

        # Game state
        game_over = False

        while not game_over:
            # Add a new color to the sequence at the start of each round
            new_color = random.choice(range(4))
            game_sequence.append(new_color)

            # Play the sequence to the player
            for color in game_sequence:
                # leds[color].value = True
                rfm95.send(bytes(packets[color], "UTF-8"))
                audio.play(sounds[color])
                time.sleep(playback_delay_time)
                # leds[color].value = False
                rfm95.send(bytes("O", "UTF-8"))
                time.sleep(playback_delay_time)

            # Get the player's response
            for color in game_sequence:
                button_pressed = False
                while not button_pressed:
                    # for i, (button, packet) in enumerate(zip(buttons, packets)):
                    for i, button in enumerate(buttons):
                        button_event = button.events.get()  # Get the button press event
                        if button_event and button_event.pressed:  # Button is pressed
                            button_pressed = True
                            if button == ModeButton:  # Player pressed the mode button
                                print("Mode button pressed")
                                exit_game = True
                            elif i != color:  # Player pressed the wrong button
                                game_over = True
                            else:
                                # leds[i].value = True  # Light up the LED when the button is pressed
                                audio.play(sounds[i])  # Play the sound when the button is pressed
                                rfm95.send(bytes(packets[color], "UTF-8"))  # Send the corresponding packet
                                print("packet sent")
                                time.sleep(player_delay_time)
                                rfm95.send(bytes("O", "UTF-8"))
                                # while button.events.get() and button.events.get().pressed:  # Keep the LED lit as long as the button is pressed
                                #     pass
                                # leds[i].value = False  # Turn off the LED when the button is released
                            break
                if exit_game:
                    print("Exiting game sequence")
                    break
                if game_over:
                    break

            if exit_game:
                print("Exiting round")
                break

            # Add a delay after the user inputs the correct sequence
            if not game_over:
                time.sleep(1)
                round_counter += 1
                if round_counter % 2 == 0:  # After every 2 rounds
                    playback_delay_time *= 0.8  # Decrease the delay time by 20%

        if exit_game:
            print("Exiting Simon game mode")
            break

        # Game over, play LOSE sound and flash all LEDs
        audio.play(loseWav)  # Play the LOSE sound
        for _ in range(2):
            for led in leds:
                led.value = True
                rfm95.send(bytes("R", "UTF-8"))
                rfm95.send(bytes("Y", "UTF-8"))
                rfm95.send(bytes("G", "UTF-8"))
            time.sleep(0.1)
            for led in leds:
                led.value = False
                rfm95.send(bytes("O", "UTF-8"))
            time.sleep(0.1)

        # Reset the delay time and round counter for the next game
        playback_delay_time = 0.5
        round_counter = 0

        # Delay before restarting the game
        time.sleep(3)

while True:
    # Run the function for the current mode
    if modes[current_mode] == "ControllerMode":
        ControllerMode()
    elif modes[current_mode] == "SimonGame":
        SimonGame()

    # Switch to the next mode
    current_mode = (current_mode + 1) % len(modes)
    print(f"Switched to {modes[current_mode]}")
