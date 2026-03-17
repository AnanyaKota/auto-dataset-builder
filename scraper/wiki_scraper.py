import os
import requests
import uuid
from bs4 import BeautifulSoup
from urllib.parse import quote


def download_from_wiki(keyword, num, folder):

    query = quote(keyword)

    url = (
        "https://commons.wikimedia.org/w/index.php?"
        f"search={query}&title=Special:MediaSearch&type=image"
    )

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

        if "http" not in src:
            src = "https:" + src

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