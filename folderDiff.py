import os
import hashlib
import time
from datetime import datetime

date_str = datetime.now().strftime("%Y-%m-%d")
def get_file_hash(file_path):
    """Generate SHA256 hash for a given file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_files_with_hash(folder):
    """Get a dictionary of file hashes for a given folder."""
    file_hashes = {}
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_hashes[file] = get_file_hash(file_path)
    return file_hashes


def find_new_files(folder1, folder2):
    """Find files that are in folder2 but not in folder1."""
    folder1_files = get_files_with_hash(folder1)
    folder2_files = get_files_with_hash(folder2)

    new_files = {file: hash for file, hash in folder2_files.items() if hash not in folder1_files.values()}
    return new_files


def delete_duplicate_files(folder1, folder2):
    """Delete files from folder2 that also exist in folder1."""
    folder1_files = get_files_with_hash(folder1)
    folder2_files = get_files_with_hash(folder2)

    for file, hash in folder2_files.items():
        if hash in folder1_files.values():
            file_path = os.path.join(folder2, file)
            os.remove(file_path)
            print(f"Deleted: {file_path}")


if __name__ == "__main__":
    # Folder 1: The reference folder containing original files
    folder1 = "trainingData/MIDLANDS"  # Replace with actual path

    # Folder 2: The target folder to compare, containing potentially new or duplicate files
    folder2 = f"trainingdata/MIDLANDS/{date_str}"  # Replace with actual path

    new_files = find_new_files(folder1, folder2)
    print("New files in folder2:", list(new_files.keys()))

    delete_duplicate_files(folder1, folder2)
