import RPi.GPIO as GPIO
import time

BUZZER = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

p = GPIO.PWM(BUZZER, 30)
p.start(50)

try:
    while True:
        p.start(50)
        p.ChangeFrequency(262)
        time.sleep(0.3)
        p.ChangeFrequency(293)
        time.sleep(0.3)
        p.ChangeFrequency(330)
        time.sleep(0.3)
        p.ChangeFrequency(349)
        time.sleep(0.3)
        p.ChangeFrequency(392)
        time.sleep(0.3)
        p.ChangeFrequency(440)
        time.sleep(0.3)
        p.ChangeFrequency(494)
        time.sleep(0.3)
        p.ChangeFrequency(523)
        time.sleep(0.3)
        p.stop()
        time.sleep(0.3)
        

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()
