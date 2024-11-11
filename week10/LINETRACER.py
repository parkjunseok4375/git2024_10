import cv2
import numpy as np

def main():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while camera.isOpened():
        ret, frame = camera.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1) 
        frame = cv2.flip(frame, 0)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([15, 150, 150])
        upper_yellow = np.array([35, 255, 255])

        lower_white = np.array([0, 0, 180])
        upper_white = np.array([180, 25, 255])

        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_white = cv2.inRange(hsv, lower_white, upper_white)

        mask = cv2.bitwise_or(mask_yellow, mask_white)

        result = cv2.bitwise_and(frame, frame, mask=mask)

        
        combined = np.zeros_like(frame)
        combined[mask > 0] = result[mask > 0]

        cv2.imshow("Original Video", frame)
        cv2.imshow("Detected Lines", combined)

        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
