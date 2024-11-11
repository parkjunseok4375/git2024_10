import cv2  

def main():
  
    camera = cv2.VideoCapture(0)  
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  
    camera.set(cv2.CAP_PROP_FPS,30)  

    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

   

  
    while camera.isOpened():
       
        _, image = camera.read()
       
        
        image = cv2.flip(image, 1) 
        image = cv2.flip(image, 0)
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  

            roi_gray = gray[y:y + h, x:x + w]
            roi_color = image[y:y + h, x:x + w]

       
        cv2.imshow('camera test', image)  

       
        if cv2.waitKey(1) == ord('q'):
            break  

   
    cv2.destroyAllWindows()  


if __name__ == '__main__':
    main()  