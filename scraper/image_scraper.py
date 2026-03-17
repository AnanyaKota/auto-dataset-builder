import os

from scraper.bing_scraper import download_from_bing
from scraper.wiki_scraper import download_from_wiki
from scraper.unsplash_scraper import download_from_unsplash


def download_images(keyword, num_images=20):

    folder = f"dataset/raw/{keyword}"
    os.makedirs(folder, exist_ok=True)

    while True:

        current = len(os.listdir(folder))

        print("Current:", current)

        if current >= num_images:
            break

        need = num_images - current

        print("Need:", need)

        # try unsplash
        download_from_unsplash(
            keyword,
            need,
            folder
        )

        current = len(os.listdir(folder))

        if current >= num_images:
            break

        need = num_images - current

        # try wiki
        download_from_wiki(
            keyword,
            need,
            folder
        )

        current = len(os.listdir(folder))

        if current >= num_images:
            break

        need = num_images - current

        # try bing
        download_from_bing(
            keyword,
            need,
            folder
        )

        current = len(os.listdir(folder))

        if current >= num_images:
            break

        # safety stop
        if need <= 0:
            break

    print("DONE:", len(os.listdir(folder)))