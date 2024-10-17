import RPi.GPIO as GPIO
import time

SW1 = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

prev_state = 0

try:
    while True:
        current_state = GPIO.input(SW1)

        if current_state == 1 and prev_state == 0:
            print("1")
        elif current_state == 0 and prev_state == 1:
            print("0")

        prev_state = current_state 
        time.sleep(0.1)  

except KeyboardInterrupt:
    pass

GPIO.cleanup()
