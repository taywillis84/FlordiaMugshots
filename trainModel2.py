import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Step 1: Preprocess Image
def preprocess_image(image_path, target_size=(224, 224)):
    # Read image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

    # Resize image to a fixed size (e.g., 224x224)
    img_resized = cv2.resize(img, target_size)

    # Extract color histogram (this will focus on color distribution)
    hist_r = cv2.calcHist([img_resized], [0], None, [256], [0, 256])  # Red channel
    hist_g = cv2.calcHist([img_resized], [1], None, [256], [0, 256])  # Green channel
    hist_b = cv2.calcHist([img_resized], [2], None, [256], [0, 256])  # Blue channel

    # Normalize histograms
    hist_r /= hist_r.sum()
    hist_g /= hist_g.sum()
    hist_b /= hist_b.sum()

    # Visualize histogram
    plt.figure(figsize=(10, 6))
    plt.plot(hist_r, color='red', label="Red")
    plt.plot(hist_g, color='green', label="Green")
    plt.plot(hist_b, color='blue', label="Blue")
    plt.title("Color Histograms")
    plt.legend()
    plt.show()

    # Return the processed image (and histograms if needed)
    return img_resized, (hist_r, hist_g, hist_b)

# Step 2: Create CNN Model
def create_cnn_model(input_shape=(224, 224, 3)):
    model = models.Sequential([
        layers.InputLayer(input_shape=input_shape),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(6, activation='softmax')  # Adjust number of output classes based on counties
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Step 3: Prepare Data for Training
def prepare_data(train_dir, val_dir, target_size=(224, 224)):
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,  # Normalize pixel values to [0, 1]
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=target_size,
        batch_size=32,
        class_mode='sparse'
    )

    validation_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=target_size,
        batch_size=32,
        class_mode='sparse'
    )

    return train_generator, validation_generator

# Step 4: Train the Model
def train_model(model, train_generator, validation_generator, epochs=10):
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // train_generator.batch_size,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // validation_generator.batch_size,
        epochs=epochs
    )
    return history

# Step 5: Evaluate the Model
def evaluate_model(model, validation_generator):
    test_loss, test_acc = model.evaluate(validation_generator)
    print(f"Test Accuracy: {test_acc * 100:.2f}%")

# Step 6: Save the Model
def save_model(model, file_path):
    model.save(file_path)
    print(f"Model saved to {file_path}")

# Step 7: Make Prediction on New Image
def predict_background(model, image_path, target_size=(224, 224)):
    img, _ = preprocess_image(image_path, target_size)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    img = img / 255.0  # Normalize

    prediction = model.predict(img)
    predicted_class = np.argmax(prediction, axis=1)
    return predicted_class

# Main execution
if __name__ == "__main__":
    train_dir = 'OrangeCounty'  # Directory with subfolders for each county
    val_dir = 'testImage'

    # Set target size for resizing images
    target_size = (224, 224)  # Use (480, 600) or (150, 150) as needed

    # Prepare data
    train_generator, validation_generator = prepare_data(train_dir, val_dir, target_size)

    # Create and compile model
    model = create_cnn_model(input_shape=target_size + (3,))

    # Train model
    history = train_model(model, train_generator, validation_generator)

    # Evaluate model
    evaluate_model(model, validation_generator)

    # Save the model
    save_model(model, "mugshot_model.h5")


