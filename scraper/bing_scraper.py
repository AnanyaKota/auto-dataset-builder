import os
import requests
import uuid
import json

from bs4 import BeautifulSoup
from urllib.parse import quote


BAD_WORDS = [
    "cartoon",
    "anime",
    "illustration",
    "drawing",
    "vector",
    "logo",
    "icon",
    "3d",
    "render",
    "art",
    "wallpaper",
    "clipart",
    "ai",
    "generated"
]


def is_bad(url):

    u = url.lower()

    for w in BAD_WORDS:

        if w in u:
            return True

    return False


def download_from_bing(
        keyword,
        num,
        folder
):

    search_query = keyword + " photo"

    query = quote(
        search_query
    )

    url = (
        f"https://www.bing.com/images/search?"
        f"q={query}&form=HDRSC2"
    )

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(
        url,
        headers=headers
    )

    soup = BeautifulSoup(
        r.text,
        "lxml"
    )

    tags = soup.find_all(
        "a",
        {"class": "iusc"}
    )

    count = 0

    i = 0

    while (
        count < num
        and i < len(tags)
    ):

        tag = tags[i]
        i += 1

        try:

            m = tag.get("m")

            if not m:
                continue

            data = json.loads(m)

            img_url = data["murl"]

            if is_bad(img_url):
                continue

            img = requests.get(
                img_url,
                timeout=5
            ).content

            if len(img) < 5000:
                continue

            name = str(uuid.uuid4()) + ".jpg"

            path = os.path.join(
                folder,
                name
            )

            with open(path, "wb") as f:
                f.write(img)

            count += 1

        except:
            pass