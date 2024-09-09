
import pickle
import face_recognition
import cv2
import numpy as np



#test face recognition using telegram bot.

def predict(img_path, knn_clf=None, model_path=None, threshold=0.45): # 6 needs 40+ accuracy, 4 needs 60+ accuracy

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



def test_photo(pic):
    
    name='empty'
    img_re1=cv2.imread(pic,1)

    img_re=cv2.cvtColor(img_re1, cv2.COLOR_BGR2RGB)
    predictions = predict(img_re, model_path="trained_data") # add path here
    
    #no faces then:
    if predictions==[]:

        return name
    
    else:
            
        for name, (top, right, bottom, left) in predictions:
  
            
            cv2.rectangle(img_re1, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(img_re1, name, (left-10,top-6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 255), 2)
            
            
        cv2.imwrite('cash_telephoto/img_saved.jpg', img_re1)

        return name

