import os
from PIL import Image
import imagehash

clean_path = "dataset/clean"
final_path = "dataset/final"


def remove_duplicates():

    os.makedirs(final_path, exist_ok=True)

    for category in os.listdir(clean_path):

        clean_folder = os.path.join(clean_path, category)
        final_folder = os.path.join(final_path, category)

        os.makedirs(final_folder, exist_ok=True)

        hashes = set()

        for file in os.listdir(clean_folder):

            file_path = os.path.join(clean_folder, file)

            try:

                img = Image.open(file_path)

                h = imagehash.average_hash(img)

                if h in hashes:
                    continue

                hashes.add(h)

                save_path = os.path.join(final_folder, file)

                img.save(save_path)

            except:
                pass