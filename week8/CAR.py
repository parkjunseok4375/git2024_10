import threading
import serial
import time
import RPi.GPIO as GPIO

bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
gData = b""  # gData를 바이트 문자열로 초기화

def serial_thread():
    global gData
    while True:
        data = bleSerial.readline()
        if data:  # 데이터가 비어 있지 않은 경우
           
            gData = data  # 수신한 바이트 데이터를 gData에 저장

SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

PWMA = 18
PWMB = 23
AIN1 = 22
AIN2 = 27
BIN1 = 25
BIN2 = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 500)
R_Motor = GPIO.PWM(PWMB, 500)
L_Motor.start(0)
R_Motor.start(0)

def main():
    global gData
    previous_gData = b""  # 이전 gData 상태

    try:
        while True:
            if gData != previous_gData:  # gData가 변경된 경우
                previous_gData = gData  # 이전 gData 업데이트
                
                # 명령어 판별
                if gData.startswith(b'\xff'):
                    command = gData[6]  # 6번째 바이트를 명령어로 사용
                    if command == 0x04:  # 좌회전
                        print("ok left")
                        GPIO.output(AIN1,1)
                        GPIO.output(AIN2,0) #오른쪽 앞
                        GPIO.output(BIN1,0)
                        GPIO.output(BIN2,1) #왼쪽 앞
                        L_Motor.ChangeDutyCycle(50)
                        R_Motor.ChangeDutyCycle(50)
                        


                    elif command == 0x01:  # 전진
                        print("ok go")
                        GPIO.output(AIN1,0)
                        GPIO.output(AIN2,1) #오른쪽 앞
                        GPIO.output(BIN1,0)
                        GPIO.output(BIN2,1) #왼쪽 앞
                        L_Motor.ChangeDutyCycle(50)
                        R_Motor.ChangeDutyCycle(50)
                        


                    elif command == 0x08:  # 우회전
                        print("ok right")
                        GPIO.output(AIN1,0)
                        GPIO.output(AIN2,1) #오른쪽 앞
                        GPIO.output(BIN1,1)
                        GPIO.output(BIN2,0) #왼쪽 앞
                        L_Motor.ChangeDutyCycle(50)
                        R_Motor.ChangeDutyCycle(50)
                        


                    elif command == 0x02:  # 후진
                        print("ok back")
                        GPIO.output(AIN1,1)
                        GPIO.output(AIN2,0) #오른쪽 앞
                        GPIO.output(BIN1,1)
                        GPIO.output(BIN2,0) #왼쪽 앞
                        L_Motor.ChangeDutyCycle(50)
                        R_Motor.ChangeDutyCycle(50)
                        

                    elif command == 0x00:  # 정지
                        print("ok stop")
                        L_Motor.ChangeDutyCycle(0)
                        R_Motor.ChangeDutyCycle(0)

                    else:
                        print("Unknown command")  # 알 수 없는 명령어 처리

            time.sleep(0.1)  # 루프가 너무 빠르지 않도록 약간의 대기 시간 추가

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    task1 = threading.Thread(target=serial_thread)
    task1.start()
    main()
    bleSerial.close()
