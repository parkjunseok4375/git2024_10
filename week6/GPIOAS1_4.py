import RPi.GPIO as GPIO
import time

pins = [5, 6, 13, 19]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(pins[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pins[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pins[2], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pins[3], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counts = [0, 0, 0, 0]
prev_states = [0, 0, 0, 0]

try:
    while True:
        state1 = GPIO.input(pins[0])
        state2 = GPIO.input(pins[1])
        state3 = GPIO.input(pins[2])
        state4 = GPIO.input(pins[3])

        if state1 == 1 and prev_states[0] == 0:
            counts[0] += 1
            print(f"( 'SW1 click: {counts[0]}' )")

        if state2 == 1 and prev_states[1] == 0:
            counts[1] += 1
            print(f"( 'SW2 click: {counts[1]}' )")

        if state3 == 1 and prev_states[2] == 0:
            counts[2] += 1
            print(f"( 'SW3 click: {counts[2]}' )")

        if state4 == 1 and prev_states[3] == 0:
            counts[3] += 1
            print(f"( 'SW4 click: {counts[3]}' )")

        prev_states[0] = state1
        prev_states[1] = state2
        prev_states[2] = state3
        prev_states[3] = state4

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

