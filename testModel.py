import pytest
import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

folder = "trainingData/MIDLANDS/2025-03-21"


# Define the fixture to load the model
@pytest.fixture
def model():
    # Load your trained model
    model = tf.keras.models.load_model('mugshot_classifier.h5')
    return model


# Function to generate saliency map
def generate_saliency_map(model, img_array, class_index):
    """
    Generate a saliency map for the given image and class index.
    """
    img_array = tf.convert_to_tensor(img_array, dtype=tf.float32)
    img_array = tf.Variable(img_array)  # Make the image a trainable variable for gradient computation

    with tf.GradientTape() as tape:
        tape.watch(img_array)
        predictions = model(img_array)  # Get the model's predictions
        loss = predictions[0][class_index]  # Get the class score for the predicted class

    # Compute the gradient of the loss with respect to the image
    grads = tape.gradient(loss, img_array)

    # Take the absolute value of the gradients
    saliency = tf.reduce_max(tf.abs(grads), axis=-1)  # We only care about the highest gradients

    # Normalize the saliency map between 0 and 1
    saliency = saliency / tf.reduce_max(saliency)

    return saliency.numpy()


# Test function to test the model on a folder of images and show the saliency map
def test_model_on_folder(model, folder_path=folder, img_size=(224, 224)):
    # Class names based on the model's output (update this to your actual class names)
    class_names = ['Jefferson', 'Midlands', 'Orange']
    mismatches = []  # List to store mismatches
    correct_predictions = 0  # Count correct predictions
    total_predictions = 0  # Count total predictions

    # Loop through all images in the folder and predict
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)

        # Skip non-image files based on file extension
        if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Skipping non-image file: {img_name}")
            continue

        try:
            # Load and preprocess the image
            img = image.load_img(img_path, target_size=img_size)
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

            # Make prediction
            prediction = model.predict(img_array)
            predicted_class_index = np.argmax(prediction, axis=1)[
                0]  # Get the index of the class with the highest probability
            confidence = prediction[0][predicted_class_index]  # Get the confidence for the predicted class

            # Get the class name
            predicted_class_name = class_names[predicted_class_index]

            # Check if the filename contains the predicted county
            if any(county.lower() in img_name.lower() for county in class_names if county == predicted_class_name):
                correct_predictions += 1  # Increment correct prediction count
            else:
                mismatches.append(f"{img_name} | Predicted: {predicted_class_name}")
                # Generate the saliency map for the predicted class
                saliency_map = generate_saliency_map(model, img_array, predicted_class_index)

                # Display the original image and its saliency map
                plt.figure(figsize=(10, 5))

                # Plot original image
                plt.subplot(1, 2, 1)
                plt.imshow(img)
                plt.title(f"Original Image: {img_name}")
                plt.axis('off')

                # Plot saliency map
                plt.subplot(1, 2, 2)
                plt.imshow(saliency_map[0], cmap='jet')
                plt.title(f"Saliency Map\nPredicted: {predicted_class_name} ({confidence * 100:.2f}%)")
                plt.axis('off')

                plt.show()

                # Print the result
                print(
                    f"Image: {img_name} | Predicted Class: {predicted_class_name} | Confidence: {confidence * 100:.2f}%")

            total_predictions += 1  # Increment total predictions count

        except Exception as e:
            # Handle image loading errors (e.g., corrupted or unsupported image formats)
            print(f"Error loading image {img_name}: {e}")
            continue

    # Output mismatches at the end
    if mismatches:
        print("\nMISMATCHED FILES:")
        for mismatch in mismatches:
            print(mismatch)
    else:
        print("\nNo mismatches found.")

    # Report accuracy at the end
    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
    print(f"\nAccuracy Report:")
    print(f"Total Predictions: {total_predictions}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Incorrect Predictions: {total_predictions - correct_predictions}")
    print(f"Accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    # Run the test
    model = model()  # Load the model
    test_model_on_folder(model, folder_path=folder)  # Test the model on images in the folder
