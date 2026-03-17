import sys
import os
import json
import zipfile
import streamlit as st

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from scraper.image_scraper import download_images
from processor.image_cleaner import clean_images
from processor.duplicate_remover import remove_duplicates
from processor.image_processor import process_images
from processor.dataset_manager import create_dataset_info


# ---------- ZIP ----------

def zip_dataset():

    zip_path = "dataset.zip"

    with zipfile.ZipFile(zip_path, "w") as z:

        for root, _, files in os.walk("dataset"):

            for file in files:

                z.write(
                    os.path.join(root, file)
                )

    return zip_path


def zip_keyword(keyword):

    zip_path = f"{keyword}.zip"

    with zipfile.ZipFile(zip_path, "w") as z:

        for stage in [
            "raw",
            "clean",
            "final",
            "processed"
        ]:

            folder = os.path.join(
                "dataset",
                stage,
                keyword
            )

            if not os.path.exists(folder):
                continue

            for file in os.listdir(folder):

                z.write(
                    os.path.join(folder, file)
                )

    return zip_path


# ---------- CLEAR ----------

def clear_keyword(keyword):

    for stage in [
        "raw",
        "clean",
        "final",
        "processed"
    ]:

        folder = os.path.join(
            "dataset",
            stage,
            keyword
        )

        if os.path.exists(folder):

            for f in os.listdir(folder):
                os.remove(
                    os.path.join(folder, f)
                )

            os.rmdir(folder)


def clear_all():

    for stage in [
        "raw",
        "clean",
        "final",
        "processed"
    ]:

        folder = os.path.join(
            "dataset",
            stage
        )

        if os.path.exists(folder):

            for root, dirs, files in os.walk(
                folder,
                topdown=False
            ):

                for f in files:
                    os.remove(
                        os.path.join(root, f)
                    )

                for d in dirs:
                    os.rmdir(
                        os.path.join(root, d)
                    )


# ---------- UI ----------

st.title(
    "Automatic Image Dataset Generator"
)

keyword = st.text_input(
    "Enter keyword / prompt"
)

num = st.number_input(
    "Number of images",
    min_value=5,
    max_value=200,
    value=20
)


# ---------- SCRAPE ----------

if st.button("Scrape Images"):

    if keyword:

        st.write("Scraping...")

        download_images(
            keyword,
            num
        )

        folder = f"dataset/raw/{keyword}"

        if os.path.exists(folder):

            st.write(
                "Images:",
                len(os.listdir(folder))
            )

        st.success("Done")


# ---------- CLEAN ----------

if st.button("Clean Images"):

    st.write("Cleaning...")

    clean_images()

    st.success("Done")


# ---------- DUP ----------

if st.button("Remove Duplicates"):

    st.write("Removing...")

    remove_duplicates()

    st.success("Done")


# ---------- OPS ----------

st.subheader(
    "CV Operations"
)

st.caption(
    "Resize + Computer Vision filters"
)

ops = st.multiselect(
    "Operations",
    [
        "grayscale",
        "blur",
        "edge",
        "threshold"
    ]
)

size = st.number_input(
    "Resize",
    64,
    512,
    256
)


if st.button("Process Images"):

    process_images(
        ops,
        size
    )

    st.success("Processed")


# ---------- INFO ----------

if st.button(
    "Create Dataset Info"
):

    create_dataset_info()

    st.success("Created")


if st.button(
    "Show Dataset Info"
):

    path = "dataset/dataset_info.json"

    if os.path.exists(path):

        with open(path) as f:
            data = json.load(f)

        st.json(data)


# ---------- PIPELINE ----------

if st.button(
    "Run Full Pipeline"
):

    if keyword:

        st.write("Scraping...")
        download_images(
            keyword,
            num
        )

        st.write("Cleaning...")
        clean_images()

        st.write("Removing...")
        remove_duplicates()

        st.write("Processing...")
        process_images(
            ops,
            size
        )

        create_dataset_info()

        st.success("Done")

    else:

        st.warning(
            "Enter keyword"
        )


# ---------- DOWNLOAD ----------

st.subheader("Download")

if st.button(
    "Download Full Dataset"
):

    path = zip_dataset()

    with open(path, "rb") as f:

        st.download_button(
            "Download",
            f,
            "dataset.zip"
        )


if st.button(
    "Download Keyword"
):

    if keyword:

        path = zip_keyword(keyword)

        with open(path, "rb") as f:

            st.download_button(
                "Download",
                f,
                f"{keyword}.zip"
            )


# ---------- CLEAR ----------

st.subheader("Clear")

if st.button(
    "Clear Keyword"
):

    if keyword:

        clear_keyword(keyword)

        st.success("Cleared")


if st.button(
    "Clear All"
):

    clear_all()

    st.success("Cleared")


# ---------- VIEW ----------

st.subheader("View")

stage = st.selectbox(
    "Stage",
    [
        "raw",
        "clean",
        "final",
        "processed"
    ]
)

base = f"dataset/{stage}"


def stage_message(stage):

    if stage == "raw":
        return "Scrape first"

    if stage == "clean":
        return "Run Clean first"

    if stage == "final":
        return "Remove duplicates first"

    if stage == "processed":
        return "Process first"


if keyword:

    folder = os.path.join(
        base,
        keyword
    )

    if not os.path.exists(folder):

        st.warning(
            stage_message(stage)
        )

    else:

        files = os.listdir(folder)

        if len(files) == 0:

            st.warning(
                stage_message(stage)
            )

        else:

            st.write(
                "Total:",
                len(files)
            )

            cols = st.columns(4)

            for i, file in enumerate(
                files[:12]
            ):

                cols[
                    i % 4
                ].image(
                    os.path.join(
                        folder,
                        file
                    ),
                    use_container_width=True
                )