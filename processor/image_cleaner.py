import os
import cv2
from PIL import Image


raw_path = "dataset/raw"
clean_path = "dataset/clean"


def is_valid_image(path):
    try:
        img = Image.open(path)
        img.verify()
        return True
    except:
        return False


def clean_images():

    os.makedirs(clean_path, exist_ok=True)

    for category in os.listdir(raw_path):

        raw_folder = os.path.join(raw_path, category)
        clean_folder = os.path.join(clean_path, category)

        os.makedirs(clean_folder, exist_ok=True)

        for file in os.listdir(raw_folder):

            file_path = os.path.join(raw_folder, file)

            if not is_valid_image(file_path):
                print("Bad image:", file)
                continue

            img = cv2.imread(file_path)

            if img is None:
                print("Corrupt:", file)
                continue

            h, w, _ = img.shape

            if h < 100 or w < 100:
                print("Too small:", file)
                continue

            save_path = os.path.join(clean_folder, file)

            cv2.imwrite(save_path, img)

            print("Saved:", file)


if __name__ == "__main__":
    clean_images()