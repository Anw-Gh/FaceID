import cv2,time
import pickle
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from datetime import datetime

from attendance import attendance
# from send_name import send_names
import telebot
bot = telebot.TeleBot("API_KEY")

def predict(img_path, knn_clf=None, model_path=None, threshold=0.45): # 6 needs 40+ accuracy, 4 needs 60+ accuracy

# if file is empty..
    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")


    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    img = img_path
    face_box = face_recognition.face_locations(img)

    # If no faces are found in the image, return an empty result.
    if len(face_box) == 0:
        
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(img, known_face_locations=face_box)


    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=2)
    matches = [closest_distances[0][i][0] <= threshold for i in range(len(face_box))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings),face_box,matches
    )]


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
name=''
skip_fr=0
write_done=False
img_re=False
FONT = cv2.FONT_HERSHEY_DUPLEX


webcam = cv2.VideoCapture(0,cv2.CAP_DSHOW) #  0 to use webcam 
while True:

    # Loop until the camera is working
    rval = False

    while(not rval):

        # Put the image from the webcam into 'frame'
        (rval, frame) = webcam.read()

        if(not rval):
            print("Failed to open webcam. Trying again...")
            
    
    # Flip the image (optional)
    frame=cv2.flip(frame,1) # 0 = horizontal ,1 = vertical , -1 = both
    frame_copy = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    gray = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)
    
    #detect faces.
    faces = face_cascade.detectMultiScale(gray, 1.1, 2)
    
    #FILLED rectangle to put some info.
    cv2.rectangle(frame,(0,435), (638,480), (0,0,0),cv2.FILLED)

    
    currentDateAndTime = datetime.now()
    cur_min = currentDateAndTime.minute
    
    if len(faces) != 1:
        cv2.putText(frame, 'Welcome, Please stand in front of the camera..', (0,465), FONT, 0.8, (255, 255, 255), 1)
        name=''
        
    
    else:
        # if one face only.
        
        for(x, y, w, h) in faces:
                
            x*=4
            y*=4
            w*=4
            h*=4
                
            #take photo every 10 frame.
            if skip_fr%30==0:
                write_done=cv2.imwrite('cash_photo/saved_cash.jpg',frame[y:(y+h),x:(x+w)])
               
        
        #read the image and encoded it using predict()
        if write_done is True:
             img_re=cv2.imread('cash_photo/saved_cash.jpg',1)
                    
             predictions = predict(img_re, model_path="model/trained_model") # add path here        
             for name, (top, right, bottom, left) in predictions:
                 name=name
                 # send_names(name)
                 if name=='unknown':
                     if skip_fr%30==0:
                         print('skipped')
                         bot.send_message(397728079,'🛑🛑WARNING, unknown person is trying to enter the company🛑🛑')
                         bot.send_photo(397728079, photo=open('cash_photo/saved_cash.jpg', 'rb'))
                        

        
        #no name, or more than one face
        if name == '':
            cv2.rectangle(frame, (x, y), ((x+w), (y+h)), (0, 0, 0), 6)
            cv2.putText(frame, 'Looking for face, must be ONE person..', (0,465), FONT, 0.8, (255, 255, 255), 1)
                       
            
        elif name == 'unknown':
            cv2.rectangle(frame, (x, y), ((x+w), (y+h)), (0, 0, 255), 2)  
            cv2.putText(frame, name, (0,465), FONT, 0.8, (255, 255, 255), 1)    
            cv2.imwrite('unknown_people/unknown_'+str(cur_min)+'.jpg', frame[y:(y+h),x:(x+w)])
      
        #known face.
        else:
            cv2.rectangle(frame, (x, y), ((x+w), (y+h)), (0, 255, 0), 2)  
            cv2.putText(frame, name, (0,465), FONT, 0.8, (255, 255, 255), 1)
            cv2.imwrite(f'known_people/im_{name}_'+str(cur_min)+'.jpg',frame[y:(y+h),x:(x+w)])
            attendance(name+str(cur_min))

        
        
    skip_fr+=1 
    write_done = False
    img_re=False
    is_unknown=False
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
webcam.release()
cv2.destroyAllWindows()

