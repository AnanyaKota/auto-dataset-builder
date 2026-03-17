import os
import json
from datetime import datetime

processed_path = "dataset/processed"
info_file = "dataset/dataset_info.json"


def create_dataset_info():

    data = {}
    total = 0

    for category in os.listdir(processed_path):

        folder = os.path.join(processed_path, category)

        if not os.path.isdir(folder):
            continue

        images = os.listdir(folder)

        count = len(images)

        total += count

        data[category] = {
            "image_count": count,
            "created_at": str(datetime.now())
        }

    data["TOTAL"] = total

    with open(info_file, "w") as f:
        json.dump(data, f, indent=4)

    print("Saved info")