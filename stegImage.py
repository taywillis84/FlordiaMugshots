from PIL import Image
import numpy as np

def message_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message)

def encode_message(image_path, message, output_path):
    image = Image.open(image_path)
    pixels = np.array(image, dtype=np.uint8)  # Ensure correct dtype

    binary_message = message_to_binary(message) + '1111111111111110'  # End marker
    binary_index = 0

    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(pixels.shape[2]):  # RGB channels
                if binary_index < len(binary_message):
                    new_value = (int(pixels[i, j, k]) & ~1) | int(binary_message[binary_index])
                    pixels[i, j, k] = np.clip(new_value, 0, 255)  # Ensure valid range
                    binary_index += 1
                if binary_index >= len(binary_message):
                    break

    encoded_image = Image.fromarray(pixels)
    encoded_image.save(output_path)
    print(f"Message encoded and saved to {output_path}")

# Example Usage
encode_message('newPhotosTest/ALBANO_JEFFREY_JOSEPH',
               'Testing with encoded message. This message is intended to disrupt the AI models capabilities to detect an image as being from Orange County, Florida.',
               'newPhotosTest/encoded.png')
