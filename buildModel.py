import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt


def prepare_data(folder_path, img_size=(224, 224), batch_size=32):
    """
    Prepare and augment image data for training
    """
    # Create data generator with augmentation
    datagen = ImageDataGenerator(
        rescale=1. / 255,
        validation_split=0.2,  # 20% for validation
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    # Training generator
    train_generator = datagen.flow_from_directory(
        folder_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',  # Changed to categorical for 3 classes
        subset='training',
        shuffle=True
    )

    # Validation generator
    validation_generator = datagen.flow_from_directory(
        folder_path,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',  # Changed to categorical for 3 classes
        subset='validation',
        shuffle=True
    )

    return train_generator, validation_generator


def build_model(input_shape=(224, 224, 3), num_classes=3):
    """
    Build CNN model architecture
    """
    model = Sequential([
        # First Convolutional Block
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D(2, 2),

        # Second Convolutional Block
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),

        # Third Convolutional Block
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),

        # Flatten and Dense layers
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')  # Changed to softmax for 3 classes
    ])

    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',  # Changed to categorical_crossentropy
        metrics=['accuracy']
    )

    return model


def plot_training_history(history, output_path='training_history.png'):
    """
    Plot and save training history
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()

    # Plot loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    # Configuration
    folder_path = 'trainingData'  # Replace with your folder path
    img_size = (224, 224)
    batch_size = 32
    epochs = 50
    num_classes = 3  # Added number of classes

    # Expected folder structure:
    # trainingData/
    #   category1/
    #   category2/
    #   category3/

    # Prepare data
    print("Preparing data...")
    train_generator, validation_generator = prepare_data(
        folder_path,
        img_size=img_size,
        batch_size=batch_size
    )

    # Build model
    print("Building model...")
    model = build_model(input_shape=(*img_size, 3), num_classes=num_classes)
    model.summary()

    # Train model
    print("Training model...")
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        validation_steps=validation_generator.samples // batch_size
    )

    # Save model
    modelName = "mugshot_classifier.h5"
    model.save(modelName)
    print(f"Model saved as {modelName}")

    # Plot and save training history
    plot_training_history(history)
    print("Training history plot saved as 'training_history.png'")

    # Evaluate model
    print("\nFinal evaluation:")
    train_loss, train_acc = model.evaluate(train_generator)
    val_loss, val_acc = model.evaluate(validation_generator)

    print(f"Training accuracy: {train_acc:.4f}")
    print(f"Validation accuracy: {val_acc:.4f}")


if __name__ == "__main__":
    main()