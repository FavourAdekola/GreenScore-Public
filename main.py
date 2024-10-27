import cv2 as cv
import tensorflow as tf
import numpy as np
import time
import webbrowser
import requests


model = tf.keras.models.load_model('trained_model/trained_model.keras')

IMG_SIZE = (224, 224)
PREDICTION_INTERVAL = 5
FLASH_DURATION = 1.5

last_flash_time = 0
curr_user = ""

def add_points():
    if curr_user != "":
        response = requests.get("https://greenscore.onrender.com/api/user/" + curr_user + "/points")
    

    # Post Request for user points to be updates
    curr_points = response.json()
    curr_points['points'] += 1
    
    response = requests.post("https://greenscore.onrender.com/api/user/" + curr_user + "/points", json={'points' : curr_points['points']})
    print(response)



def preprocess_frame(frame, img_size=(224, 224)):
    # Resize image to the expected input size of the model
    frame = cv.resize(frame, img_size)
    
    # Convert image to RGB (OpenCV loads as BGR)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    # Scale pixel values to [0, 1] if necessary
    frame = frame / 255.0
    
    # Add batch dimension (model expects shape: (batch, height, width, channels))
    frame = np.expand_dims(frame, axis=0)
    
    return frame

def predict_frame(frame):
    # Preprocess the image
    processed_frame = preprocess_frame(frame)
    
    # Pass the image through the model to get predictions
    predictions = model.predict(processed_frame)
    
    # Get the predicted class (index with highest probability)
    predicted_class = np.argmax(predictions, axis=1)[0]
    predicted_prob = predictions[0][predicted_class]
    
    return predicted_class, predicted_prob

# Example usage
cap = cv.VideoCapture(0)
# initialize the cv2 QRCode detector 
detector = cv.QRCodeDetector()

last_prediction_time = time.time()


print("Press 'q' to exit")

while cap.isOpened():
    ret,frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    current_time = time.time()
    flash_green = False

    if current_time - last_prediction_time > PREDICTION_INTERVAL:
        predicted_class, predicted_prob = predict_frame(frame)
        print(f"Predicted Class: {predicted_class}, Probability: {predicted_prob}")
        #{'cardboard': 0, 'glass': 1, 'metal': 2, 'paper': 3, 'plastic': 4, 'trash': 5}

        if predicted_prob > 0.98 and predicted_class != 5:
            flash_green = True
            last_flash_time = current_time
            if curr_user  != "":
                add_points()

        last_prediction_time = current_time
    
    if flash_green and current_time - last_flash_time < FLASH_DURATION:
        overlay = frame.copy()
        overlay[:] = (0,255,0)
        cv.addWeighted(overlay,0.5,frame,0.5,0,frame)
    
    data, bbox, _ = detector.detectAndDecode(frame) 
    # check if there is a QRCode in the image 
    if data and bbox is not None: 
        curr_user = str(data)
        print("User Changed")
    
    cv.imshow("Webcam Feed", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()



