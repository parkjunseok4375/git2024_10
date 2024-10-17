import RPi.GPIO as GPIO
import time

SW1 = 5
BUZZER = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BUZZER, GPIO.OUT)

p = GPIO.PWM(BUZZER, 100)       

  

try:
    while True:
        sw1Value = GPIO.input(SW1)  
        if sw1Value == 1:  # 버튼이 눌리면
            p.start(50) 
            p.ChangeFrequency(100)
            time.sleep(0.5)  
            p.stop() # 소리 멈춤
            time.sleep(1)



         

except KeyboardInterrupt:  
    pass  

GPIO.cleanup()  
