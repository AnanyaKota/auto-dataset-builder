import os
import requests
import uuid
from urllib.parse import quote
from bs4 import BeautifulSoup


def download_from_unsplash(keyword, num, folder):

    query = quote(keyword)

    url = f"https://unsplash.com/s/photos/{query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")

    imgs = soup.find_all("img")

    count = 0

    for img in imgs:

        if count >= num:
            break

        src = img.get("src")

        if not src:
            continue

        if "images.unsplash.com" not in src:
            continue

        try:

            data = requests.get(src, timeout=5).content

            if len(data) < 5000:
                continue

            name = str(uuid.uuid4()) + ".jpg"

            path = os.path.join(folder, name)

            with open(path, "wb") as f:
                f.write(data)

            count += 1

        except:
            pass