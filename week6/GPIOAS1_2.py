import RPi.GPIO as GPIO
import time

SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        if GPIO.input(SW1) == 1:
            print("click 1")
            time.sleep(0.5)

        if GPIO.input(SW2) == 1:
            print("click 2")
            time.sleep(0.5)

        if GPIO.input(SW3) == 1:
            print("click 3")
            time.sleep(0.5)

        if GPIO.input(SW4) == 1:
            print("click 4")
            time.sleep(0.5)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
