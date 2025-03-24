import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import cv2


def load_and_preprocess_image(image_path, target_size=(224, 224)):
    """
    Load and preprocess an image for the model
    """
    preprocess = lambda x: tf.image.resize(x, target_size) / 255.0

    image = Image.open(image_path).convert('RGB')
    input_tensor = tf.convert_to_tensor(np.array(image))
    input_tensor = preprocess(input_tensor)
    input_tensor = tf.expand_dims(input_tensor, 0)
    return input_tensor, image


def generate_saliency_map(model, img_array, class_index):
    """
    Generate a saliency map for the given image and specific class index.
    """
    img_array = tf.convert_to_tensor(img_array, dtype=tf.float32)
    img_array = tf.Variable(img_array)

    with tf.GradientTape() as tape:
        tape.watch(img_array)
        predictions = model(img_array)
        loss = predictions[0][class_index]

    grads = tape.gradient(loss, img_array)
    saliency = tf.reduce_max(tf.abs(grads), axis=-1)
    saliency = saliency / tf.reduce_max(saliency)

    return saliency.numpy()


def plot_saliency_map(saliency_map, output_path, title):
    """
    Plot and save the saliency map
    """
    saliency_map = saliency_map.squeeze()

    plt.figure(figsize=(5, 5))
    plt.imshow(saliency_map, cmap='jet')
    plt.title(title)
    plt.axis('off')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()


def average_saliency_maps(saliency_maps, standard_size, output_path, class_name):
    """
    Average multiple saliency maps after resizing to a standard size and save the result
    """
    resized_maps = [cv2.resize(map.squeeze(), standard_size) for map in saliency_maps]
    averaged_map = np.mean(np.stack(resized_maps, axis=0), axis=0)
    averaged_map = averaged_map / np.max(averaged_map)

    plt.figure(figsize=(5, 5))
    plt.imshow(averaged_map, cmap='jet')
    plt.title(f'Averaged Saliency Map ({class_name} Class)')
    plt.axis('off')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()


# Main execution
if __name__ == "__main__":
    # Load your custom model
    model_path = "mugshot_classifier.h5"
    model = load_model(model_path)

    # Class name to index mapping
    CLASS_MAP = {
        'jefferson': 0,
        'midlands': 1,
        'orange': 2
    }

    # Get class name from user input
    class_name = ("jefferson").lower()

    # Validate and set class index
    if class_name not in CLASS_MAP:
        print("Invalid class name. Please enter Orange, Midland, or Jefferson.")
        exit(1)
    CLASS_INDEX = CLASS_MAP[class_name]

    # Set directory based on class name
    image_dir = f"newImages/{class_name.capitalize()}"
    output_dir = f"saliency_maps/{class_name.capitalize()}"
    os.makedirs(output_dir, exist_ok=True)

    # List to store all saliency maps
    all_saliency_maps = []

    # Define a standard size for averaging
    STANDARD_SIZE = (224, 224)

    # Process each image in directory
    for image_file in os.listdir(image_dir):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_dir, image_file)
            output_path = os.path.join(output_dir, f"saliency_{image_file}")

            try:
                # Load and preprocess image
                input_tensor, original_image = load_and_preprocess_image(image_path)

                # Generate saliency map for specified class
                saliency_map = generate_saliency_map(model, input_tensor, CLASS_INDEX)

                # Resize saliency map to original image size for individual output
                resized_saliency = cv2.resize(saliency_map.squeeze(),
                                              (original_image.size[0], original_image.size[1]))

                # Store the saliency map (unresized) for averaging
                all_saliency_maps.append(saliency_map)

                # Save individual saliency map with class-specific title
                plot_saliency_map(resized_saliency, output_path,
                                  f'Saliency Map ({class_name.capitalize()} Class)')
                print(f"Processed: {image_file} for {class_name.capitalize()} class")

            except Exception as e:
                print(f"Error processing {image_file}: {str(e)}")

    # Generate and save the averaged saliency map
    if all_saliency_maps:
        averaged_output_path = os.path.join(output_dir, "averaged_saliency_map.png")
        average_saliency_maps(all_saliency_maps, STANDARD_SIZE, averaged_output_path, class_name.capitalize())
        print(f"Generated averaged saliency map: {averaged_output_path}")
    else:
        print("No saliency maps were generated to average")