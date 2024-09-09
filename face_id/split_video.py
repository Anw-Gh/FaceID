import cv2


#split video evrey 10 frame.
def split(path,vid):
        
    capture = cv2.VideoCapture(vid)
     
    frameNr = 1
     
    while (True):
     
        success, frame = capture.read()
     
        if success:
            if frameNr%10==0:
                
                cv2.imwrite(f'{path}/{frameNr}.jpg', frame)
     
        else:
            break
     
        frameNr = frameNr+1
     
    capture.release()