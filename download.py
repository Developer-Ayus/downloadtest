import streamlit as st
import yt_dlp
import os

st.title("📥 Universal Video/Audio Downloader")

url = st.text_input("Enter downloadable URL")

format_choice = st.selectbox(
    "Select download format",
    ["mp3", "m4a", "wav", "mp4", "webm"]
)

if format_choice in ["mp3", "m4a", "wav"]:
    quality_choice = st.selectbox(
        "Select audio quality (kbps)",
        ["64", "128", "192", "256", "320"]
    )
else:
    quality_choice = st.selectbox(
        "Select video quality",
        ["144", "240", "360", "480", "720", "1080", "1440", "2160"]
    )

if st.button("Download"):
    if url.strip():
        try:
            with st.spinner("Downloading..."):
                temp_dir = "downloads"
                os.makedirs(temp_dir, exist_ok=True)

                if format_choice in ["mp3", "m4a", "wav"]:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': format_choice,
                            'preferredquality': quality_choice,
                        }],
                    }
                else:
                    ydl_opts = {
                        'format': f"bestvideo[height<={quality_choice}]+bestaudio/best",
                        'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                        'merge_output_format': format_choice
                    }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url.strip(), download=True)
                    file_path = ydl.prepare_filename(info)
                    if format_choice in ["mp3", "m4a", "wav"]:
                        file_path = os.path.splitext(file_path)[0] + f".{format_choice}"

            # Give download link to user
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"📂 Download {os.path.basename(file_path)}",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="application/octet-stream"
                )

            st.success(f"✅ File ready: {os.path.basename(file_path)}")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please enter a valid URL")
