import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model


# Step 1: Preprocess Image
def preprocess_image(image_path, target_size=(224, 224)):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB
    img_resized = cv2.resize(img, target_size)
    return img_resized


# Step 2: Load the Model
def load_trained_model(model_path):
    return load_model(model_path)


# Step 3: Generate Class Labels from Folder Names
def generate_class_labels_from_folders(folder_path):
    return {i: folder for i, folder in enumerate(os.listdir(folder_path)) if os.path.isdir(os.path.join(folder_path, folder))}


# Step 4: Make Prediction on New Image
def predict_county(model, image_path, target_size=(224, 224), class_labels=None, confidence_threshold=0.70):
    img = preprocess_image(image_path, target_size)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    img = img / 255.0  # Normalize the image

    prediction = model.predict(img, verbose=0)
    predicted_class = np.argmax(prediction, axis=1)
    confidence = np.max(prediction)

    if confidence < confidence_threshold:
        return "No confident predictions", confidence

    predicted_county = class_labels[predicted_class[0]] if class_labels else predicted_class[0]
    return predicted_county, confidence


# Step 5: Process All Images in a Folder
def predict_images_in_folder(model, folder_path, target_size=(224, 224), class_labels=None, confidence_threshold=0.70):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png'))]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        predicted_county, confidence = predict_county(model, image_path, target_size, class_labels, confidence_threshold)

        print(f"Image: {image_file} -> Predicted County: {predicted_county} (Confidence: {confidence * 100:.2f}%)")


# Step 6: Main Function to Run the Script
if __name__ == "__main__":
    model_path = 'mugshot_model.h5'
    test_folder_path = 'newPhotosTest'  # Modify with your actual folder path

    os.makedirs(test_folder_path, exist_ok=True)

    model = load_trained_model(model_path)
    class_labels = generate_class_labels_from_folders('trainingData')  # Modify with your training data folder

    predict_images_in_folder(model, test_folder_path, class_labels=class_labels)
