import cv2 as cv
import numpy as np
import threading
import time
import SDcar

enable_linetracing = True 
is_running = False
speed = 30 

def func_thread():
    while True:
        print("LIVE")    
        time.sleep(1)
        if not is_running:
            break

def key_cmd(which_key):
    global enable_linetracing  # 전역 변수 사용
    print('which_key:', which_key)  # 디버깅 출력
    is_exit = False
    if which_key & 0xFF == 119:  # 'w'
        print('Moving forward')
        car.motor_go(speed)
    elif which_key & 0xFF == 115:  # 's'
        print('Moving backward')
        car.motor_back(speed)
    elif which_key & 0xFF == 97:  # 'a'
        print('Turning left')     
        car.motor_left(speed)   
    elif which_key & 0xFF == 100:  # 'd'
        print('Turning right')   
        car.motor_right(speed)            
    elif which_key & 0xFF == 32:  # Space
        print('Stopping')
        car.motor_stop()
    elif which_key & 0xFF == ord('q'):  # 'q'
        print('Exiting')
        car.motor_stop()
        is_exit = True
    elif which_key & 0xFF == ord('e'):  # 'e'
        enable_linetracing = True
        print('Line tracing enabled')
    elif which_key & 0xFF == ord('w'):  # 'w'
        enable_linetracing = False
        car.motor_stop()
        print('Line tracing disabled')            
    return is_exit  

def detect_maskY_HSV(frame):
    crop_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    crop_hsv = cv.GaussianBlur(crop_hsv, (5, 5), cv.BORDER_DEFAULT)
    mask_Y = cv.inRange(crop_hsv, (20, 100, 100), (45, 255, 255))
    return mask_Y

def show_grid(img):
    h, _, _ = img.shape
    for x in v_x_grid:
        cv.line(img, (x, 0), (x, h), (0, 255, 0), 1, cv.LINE_4)

def line_tracing(cx):
    global moment, v_x
    tolerance = 0.1
    diff = 0

    if moment[0] != 0 and moment[1] != 0 and moment[2] != 0:
        avg_m = np.mean(moment)
        diff = np.abs(avg_m - cx) / v_x

    print('diff = {:.4f}'.format(diff))  # 디버깅 출력

    if diff <= tolerance:
        moment[0] = moment[1]
        moment[1] = moment[2]
        moment[2] = cx

        if v_x_grid[2] <= cx < v_x_grid[3]:
            car.motor_go(speed)
            print('Going straight')  # 디버깅 출력
        elif cx < v_x_grid[2]:
            car.motor_left(speed)
            print('Turning left')  # 디버깅 출력
        elif cx >= v_x_grid[3]:
            car.motor_right(speed)
            print('Turning right')  # 디버깅 출력
    else:
        car.motor_go(speed)
        print('Going straight (adjusting)')  # 디버깅 출력
        moment = [0, 0, 0]

def main():
    global is_running, car

    camera = cv.VideoCapture(0)
    if not camera.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    camera.set(cv.CAP_PROP_FRAME_WIDTH, v_x) 
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, v_y)

    try:
        while camera.isOpened():
            ret, frame = camera.read()
            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break
            cv.imshow('Camera Feed', frame)
            flipped_frame = cv.flip(frame, -1)
            cv.imshow('Camera Feed', flipped_frame)
            
            frame = cv.flip(frame, -1)
            crop_img = frame[180:, :]
            maskY = detect_maskY_HSV(crop_img)

            contours, _ = cv.findContours(maskY, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            if contours:
                c = max(contours, key=cv.contourArea)
                if cv.contourArea(c) > 100:  # 면적이 100 이상일 때만 처리
                    m = cv.moments(c)
                    if m['m00'] > 0:  # m['00']가 0이 아닐 때만 계산
                        cx = int(m['m10'] / m['m00'])
                        cy = int(m['m01'] / m['m00'])
                        cv.circle(crop_img, (cx, cy), 3, (0, 0, 255), -1)
                        cv.drawContours(crop_img, contours, -1, (0, 255, 0), 3)

                        if enable_linetracing:
                            line_tracing(cx)

            show_grid(crop_img)
            cv.imshow('crop_img', cv.resize(crop_img, dsize=(0, 0), fx=2, fy=2))

            is_exit = False
            which_key = cv.waitKey(20)
            if which_key > 0:
                is_exit = key_cmd(which_Skey)    
            if is_exit:
                break
    except Exception as e:
        print("오류 발생:", e)
    finally:
        global is_running
        is_running = False
        camera.release()
        cv.destroyAllWindows()

if __name__ == '__main__':
    v_x = 320
    v_y = 240
    v_x_grid = [int(v_x * i / 10) for i in range(1, 10)]
    moment = np.array([0, 0, 0])

    t_task1 = threading.Thread(target=func_thread)
    t_task1.start()

    car = SDcar.Drive()
    
    is_running = True
    main() 
    is_running = False
    t_task1.join()  # 스레드가 종료될 때까지 기다림
    car.clean_GPIO()
    print('end vis')
