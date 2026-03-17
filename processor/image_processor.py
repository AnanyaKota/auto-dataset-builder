import os
import cv2

final_path = "dataset/final"
processed_path = "dataset/processed"


def process_images(ops, size=256):

    os.makedirs(processed_path, exist_ok=True)

    for category in os.listdir(final_path):

        final_folder = os.path.join(final_path, category)
        processed_folder = os.path.join(processed_path, category)

        os.makedirs(processed_folder, exist_ok=True)

        for file in os.listdir(final_folder):

            file_path = os.path.join(final_folder, file)

            img = cv2.imread(file_path)

            if img is None:
                continue

            img = cv2.resize(img, (size, size))

            if "grayscale" in ops:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            if "blur" in ops:
                img = cv2.GaussianBlur(img, (5, 5), 0)

            if "edge" in ops:

                gray = img

                if len(img.shape) == 3:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                img = cv2.Canny(gray, 100, 200)

            if "threshold" in ops:

                gray = img

                if len(img.shape) == 3:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                _, img = cv2.threshold(
                    gray, 127, 255, cv2.THRESH_BINARY
                )

            save_path = os.path.join(
                processed_folder,
                file
            )

            cv2.imwrite(save_path, img)