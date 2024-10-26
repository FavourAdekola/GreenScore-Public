import cv2 as cv
import tensorflow as tf
import numpy as np

capture = cv.VideoCapture(0)  # 0 is the default camera
""""
while True:
    ret, frame = capture.read()  # Capture frame-by-frame
    if not ret:
        break
    
    cv.imshow('Video', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

capture.release()
cv.destroyAllWindows()
"""

model = tf.keras.models.load_model('trained_model/trained_model.keras')

def preprocess_image(image_path, img_size=(224, 224)):
    # Load image with OpenCV
    image = cv.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image at path {image_path} not found.")
    
    # Resize image to the expected input size of the model
    image = cv.resize(image, img_size)
    
    # Convert image to RGB (OpenCV loads as BGR)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    
    # Scale pixel values to [0, 1] if necessary
    image = image / 255.0
    
    # Add batch dimension (model expects shape: (batch, height, width, channels))
    image = np.expand_dims(image, axis=0)
    
    return image

def predict_image(image_path):
    # Preprocess the image
    image = preprocess_image(image_path)
    
    # Pass the image through the model to get predictions
    predictions = model.predict(image)
    
    # Get the predicted class (index with highest probability)
    predicted_class = np.argmax(predictions, axis=1)[0]
    predicted_prob = predictions[0][predicted_class]
    
    return predicted_class, predicted_prob

# Example usage
image_path = "garbage_classification/plastic/plastic9.jpg"  # Change this to your image path
predicted_class, predicted_prob = predict_image(image_path)
print(f"Predicted Class: {predicted_class}, Probability: {predicted_prob}")
#{'cardboard': 0, 'glass': 1, 'metal': 2, 'paper': 3, 'plastic': 4, 'trash': 5}