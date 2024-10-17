import RPi.GPIO as GPIO
import time

SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

BUZZER = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(BUZZER, GPIO.OUT)
p = GPIO.PWM(BUZZER, 100) 
       

try:
    while True:
        sw1Value = GPIO.input(SW1)  
        sw2Value = GPIO.input(SW2)  
        sw3Value = GPIO.input(SW3)  
        sw4Value = GPIO.input(SW4)  

        if sw1Value == 1:  # 버튼이 눌리면
            p.start(50)   # 50% 듀티 사이클
            p.ChangeFrequency(100)
            time.sleep(0.5)  # 0.1초 동안 소리 유지
            p.stop() # 소리 멈춤
            time.sleep(1)

        if sw2Value == 1:  # 버튼이 눌리면
            p.start(50)   # 50% 듀티 사이클
            p.ChangeFrequency(200)
            time.sleep(0.5)  # 0.1초 동안 소리 유지
            p.stop() # 소리 멈춤
            time.sleep(1)

        if sw3Value == 1:  # 버튼이 눌리면
            p.start(50)   # 50% 듀티 사이클
            p.ChangeFrequency(300)
            time.sleep(0.5)  # 0.1초 동안 소리 유지
            p.stop() # 소리 멈춤
            time.sleep(1)

        if sw4Value == 1:  # 버튼이 눌리면
            p.start(50)   # 50% 듀티 사이클
            p.ChangeFrequency(400)
            time.sleep(0.5)  # 0.1초 동안 소리 유지
            p.stop() # 소리 멈춤
            time.sleep(1)          



         

except KeyboardInterrupt:  
    pass  

GPIO.cleanup()  
