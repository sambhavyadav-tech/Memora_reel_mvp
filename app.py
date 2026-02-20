import streamlit as st
from PIL import Image
import tempfile
import os

st.set_page_config(page_title="AI Reel Generator", layout="centered")

st.title("🎬 AI Reel Generator")
st.write("Upload multiple photos and generate a simple slideshow reel.")

# Safe MoviePy import (prevents crash at startup)
try:
    from moviepy.editor import ImageClip, concatenate_videoclips
except Exception as e:
    st.error("Video engine failed to load. Please check deployment environment.")
    st.stop()


# Upload images
uploaded_files = st.file_uploader(
    "Upload Images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Duration slider
duration = st.slider("Seconds per Image", 1, 5, 2)

# Optional vertical format toggle
vertical_mode = st.checkbox("Make it Vertical (9:16 Reel Format)")

if st.button("Generate Reel"):

    if not uploaded_files:
        st.warning("Please upload at least one image.")
        st.stop()

    clips = []
    temp_files = []

    try:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)

            # Convert to RGB to avoid PNG issues
            image = image.convert("RGB")

            # Resize if vertical mode selected
            if vertical_mode:
                image = image.resize((1080, 1920))
            else:
                image = image.resize((1280, 720))

            # Save temporary image
            temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            image.save(temp_img.name)
            temp_files.append(temp_img.name)

            clip = ImageClip(temp_img.name).set_duration(duration)
            clips.append(clip)

        # Combine clips
        final_video = concatenate_videoclips(clips, method="compose")

        # Temporary output file
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        output_path = output_file.name

        # Low resource settings for cloud
        final_video.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio=False,
            threads=1,
            preset="ultrafast",
            logger=None
        )

        st.success("Reel Generated Successfully 🎉")
        st.video(output_path)

        with open(output_path, "rb") as f:
            st.download_button(
                label="Download Reel",
                data=f,
                file_name="generated_reel.mp4",
                mime="video/mp4"
            )

    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")

    finally:
        # Cleanup temp images
        for file_path in temp_files:
            if os.path.exists(file_path):
                os.remove(file_path)
