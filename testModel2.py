import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import json
import shutil  # For moving files


# Step 1: Preprocess Image
def preprocess_image(image_path, target_size=(224, 224)):
    # Read image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

    # Resize image to a fixed size (e.g., 224x224)
    img_resized = cv2.resize(img, target_size)

    # Return the processed image
    return img_resized


# Step 2: Load the Model
def load_trained_model(model_path):
    model = load_model(model_path)
    return model


# Step 3: Generate Class Labels from Folder Names
def generate_class_labels_from_folders(folder_path):
    # Get the class labels by getting the folder names
    class_labels = {i: folder for i, folder in enumerate(os.listdir(folder_path)) if
                    os.path.isdir(os.path.join(folder_path, folder))}
    return class_labels


# Step 4: Make Prediction on New Image
def predict_county(model, image_path, target_size=(224, 224), class_labels=None, confidence_threshold=0.70):
    # Preprocess the image
    img = preprocess_image(image_path, target_size)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    img = img / 255.0  # Normalize the image

    # Get the prediction
    prediction = model.predict(img, verbose=0)
    predicted_class = np.argmax(prediction, axis=1)  # Get the index of the predicted class
    confidence = np.max(prediction)  # Get the confidence (probability) of the predicted class

    # If confidence is below threshold, return "No confident predictions"
    if confidence < confidence_threshold:
        return "No confident predictions", confidence

    # Map the predicted class index to the county name
    if class_labels is not None:
        predicted_county = class_labels[predicted_class[0]]
    else:
        predicted_county = predicted_class[0]  # Use the index directly if class_labels are not provided

    return predicted_county, confidence


# Step 5: Process All Images in a Folder
def predict_images_in_folder(model, folder_path, target_size=(224, 224), class_labels=None, confidence_threshold=0.70):
    # Get all images in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png'))]

    results = []  # List to store results as dictionaries

    # Process each image
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)

        # Make the prediction
        predicted_county, confidence = predict_county(model, image_path, target_size, class_labels,
                                                      confidence_threshold)

        # Prepare the result
        result = {
            "image": image_file,
            "predicted_county": predicted_county,
            "confidence": confidence * 100  # Convert to percentage
        }

        results.append(result)

    # Save results to JSON in the test folder
    output_json_path = os.path.join(folder_path, "_predictions_results.json")
    with open(output_json_path, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    print(f"Prediction results have been saved to '{output_json_path}'.")

    return output_json_path


# Step 6: Main Function to Run the Script
if __name__ == "__main__":
    # Path to the trained model
    model_path = 'mugshot_model.h5'

    # Folder containing the test images
    test_folder_path = 'newPhotosTest'  # Modify with your actual folder path

    # Ensure the test folder exists
    os.makedirs(test_folder_path, exist_ok=True)

    # Load the trained model
    model = load_trained_model(model_path)

    # Generate class labels from the training folder structure
    class_labels = generate_class_labels_from_folders('OrangeCounty')  # Modify with your training data folder

    # Predict for all images in the folder and save the results to JSON
    predictions_json_path = predict_images_in_folder(model, test_folder_path, class_labels=class_labels)

    # Move the prediction results JSON file into test folder
    if os.path.exists(predictions_json_path):
        destination = os.path.join(test_folder_path, "_predictions_results.json")
        shutil.move(predictions_json_path, destination)
        print(f"Moved '_predictions_results.json' to '{test_folder_path}'.")
    else:
        print("Error: Prediction results JSON file not found.")
