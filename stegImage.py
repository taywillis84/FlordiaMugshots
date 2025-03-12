from PIL import Image
import numpy as np
import os

def generate_random_data(size_in_bytes):
    """Generate a random binary string of given size (in bytes)."""
    return ''.join(format(byte, '08b') for byte in os.urandom(size_in_bytes))

def encode_message(image_path, output_path, data_size_kb=100):
    """Encodes 100KB of random data into an image using LSB steganography."""
    image = Image.open(image_path)
    pixels = np.array(image, dtype=np.uint8)  # Convert image to NumPy array

    data_size_bytes = data_size_kb * 1024  # Convert KB to bytes
    binary_message = generate_random_data(data_size_bytes) + '1111111111111110'  # End marker
    binary_index = 0

    # Iterate through pixels and modify the LSB
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(pixels.shape[2]):  # Iterate over R, G, B channels
                if binary_index < len(binary_message):
                    new_value = (int(pixels[i, j, k]) & ~1) | int(binary_message[binary_index])
                    pixels[i, j, k] = np.clip(new_value, 0, 255)  # Ensure valid range
                    binary_index += 1
                if binary_index >= len(binary_message):
                    break
        if binary_index >= len(binary_message):
            break

    # Save the modified image
    encoded_image = Image.fromarray(pixels)
    encoded_image.save(output_path)
    print(f"100 KB of data successfully encoded into {output_path}")

# Example Usage
encode_message('newPhotosTest/ALBANO_JEFFREY_JOSEPH.png', 'newPhotosTest/encoded.png')
