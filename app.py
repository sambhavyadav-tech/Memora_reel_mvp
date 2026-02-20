import streamlit as st
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image
import tempfile
import os

st.set_page_config(page_title="AI Reel Generator", layout="centered")

st.title("🎬 AI Reel Generator")
st.write("Upload your photos and generate a simple reel instantly.")

uploaded_files = st.file_uploader(
    "Upload Images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

duration = st.slider("Seconds per Image", 1, 5, 2)

if st.button("Generate Reel"):
    if uploaded_files:

        clips = []

        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            image.save(temp_file.name)

            clip = ImageClip(temp_file.name).set_duration(duration)
            clips.append(clip)

        final_video = concatenate_videoclips(clips, method="compose")

        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

        final_video.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio=False,
            verbose=False,
            logger=None
        )

        st.success("Reel Generated 🎉")
        st.video(output_path)

        with open(output_path, "rb") as file:
            st.download_button(
                "Download Reel",
                file,
                file_name="generated_reel.mp4"
            )
    else:
        st.warning("Please upload images.")
