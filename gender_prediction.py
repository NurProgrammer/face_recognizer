import cv2
from mtcnn.mtcnn import MTCNN
from keras.models import load_model
from keras_preprocessing.image import img_to_array
import numpy as np
import threading

# Initialize models and variables
detector = MTCNN()

emotion_model = "./data/_mini_XCEPTION.106-0.65.hdf5"
ageProto = "./data/age_deploy.prototxt"
ageModel = "./data/age_net.caffemodel"
genderProto = "./data/gender_deploy.prototxt"
genderModel = "./data/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']
Emotions = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

# Load models
face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
emotion_classifier = load_model(emotion_model, compile=False)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)

def ageAndgender():
    # Create a new capture for this function
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    try:
        while True:
            ret, img = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break

            default_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            faces = face_cascade.detectMultiScale(image=default_img, scaleFactor=1.3, minNeighbors=5)
            
            for (x, y, w, h) in faces:
                roi = default_img[y:y + h, x:x + w]
                if roi.size == 0:
                    continue
                    
                try:
                    blob = cv2.dnn.blobFromImage(roi, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                    
                    genderNet.setInput(blob)
                    genderPreds = genderNet.forward()
                    gender = genderList[genderPreds[0].argmax()]
                    
                    ageNet.setInput(blob)
                    agePreds = ageNet.forward()
                    age = ageList[agePreds[0].argmax()]
                    
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    label = f"{gender}, {age}"
                    cv2.putText(img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
                except Exception as e:
                    print(f"Error processing face: {e}")
                    continue

            cv2.imshow("Gender and Age Prediction", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == 27:
                break
    except Exception as e:
        print(f"Error in age and gender detection: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

def emotion():
    # Create a new capture for this function
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    try:
        while True:
            ret, img = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(image=gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                try:
                    roi = gray[y:y + h, x:x + w]
                    roi = cv2.resize(roi, (48, 48))
                    roi = roi.astype("float") / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)
                    
                    preds = emotion_classifier.predict(roi)[0]
                    emotion_probability = np.max(preds)
                    label = Emotions[preds.argmax()]
                    
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0))
                except Exception as e:
                    print(f"Error processing face: {e}")
                    continue

            cv2.imshow("Emotion Detection", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == 27:
                break
    except Exception as e:
        print(f"Error in emotion detection: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows() 