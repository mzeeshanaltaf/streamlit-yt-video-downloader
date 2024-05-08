import streamlit as st
from pytube import YouTube
import pandas as pd
import tkinter as tk
from tkinter import filedialog


def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(master=root)
    root.destroy()
    return folder_path


def download_progress_callback(stream, chunk, remaining_bytes):
    # Calculate the download percentage
    total_bytes = stream.filesize
    downloaded_bytes = total_bytes - remaining_bytes
    download_percentage = (downloaded_bytes / total_bytes) * 100
    st.session_state.progress_bar.progress(round(download_percentage),
                                           text="Download in progress. Please wait.")


def download_complete_callback(stream, fp):
    # Clear the progress bar
    st.session_state.progress_bar.empty()
    st.success("File has been downloaded successfully")


def format_views(views):
    if views < 1000:
        return views
    elif views < 1000000:
        return f"{views / 1000:.1f}K"
    else:
        return f"{views / 1000000:.1f}M"


def download_youtube_videos(yd, output_folder):
    progress_text = "Download in progress. Please wait."
    st.session_state.progress_bar = st.progress(0, text=progress_text)

    # Download YouTube video
    yd.download(output_folder)


def get_youtube_videos_details(v_url, quality):
    if "yt_df" not in st.session_state:
        st.session_state.yt_df = None
    if "yt_stream" not in st.session_state:
        st.session_state.yt_stream = None
    if "yt_thumbnail" not in st.session_state:
        st.session_state.yt_thumbnail = None
    if "progress_bar" not in st.session_state:
        st.session_state.progress_bar = None

    # Create a YouTue object
    yt = YouTube(v_url)

    # Register callback function to get download progress and completions status
    yt.register_on_progress_callback(download_progress_callback)
    yt.register_on_complete_callback(download_complete_callback)

    if quality == "Low":
        st.session_state.yt_stream = yt.streams.get_lowest_resolution()
    elif quality == "High":
        st.session_state.yt_stream = yt.streams.get_highest_resolution()

    # Get YouTube video details
    video_title = yt.title
    views = format_views(yt.views)
    length = f"{int(yt.length / 60)}:{yt.length % 60:02d}"
    channel_name = yt.author
    st.session_state.yt_thumbnail = yt.thumbnail_url

    yt_data = {'Info': ['Channel Name', 'Title', 'Length', 'Views'],
               'Details': [channel_name, video_title, length, views],
               }

    # Create a DataFrame
    st.session_state.yt_df = pd.DataFrame(yt_data)
