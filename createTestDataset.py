import os
import random
import shutil


def move_random_images(source_folder, target_folder, percentage=0.2):
    # Ensure the target folder exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # List all files in the source folder
    all_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    # Calculate how many files to move (20% of the total files)
    num_files_to_move = int(len(all_files) * percentage)

    # Randomly select the files to move
    selected_files = random.sample(all_files, num_files_to_move)

    # Move the selected files to the target folder
    for file in selected_files:
        source_path = os.path.join(source_folder, file)
        target_path = os.path.join(target_folder, file)

        # Move the file
        shutil.move(source_path, target_path)
        print(f"Moved {file} to {target_folder}")

    print(f"Moved {num_files_to_move} images to {target_folder}.")


# Example usage
source_folder = 'trainingData/MIDLANDS'  # Replace with the path to your source folder
target_folder = 'testImage/MIDLANDS'  # Replace with the path to your target folder

move_random_images(source_folder, target_folder)
