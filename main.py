from streamlit_option_menu import option_menu
from utils import *


# --- PAGE SETUP ---
# Initialize streamlit app
page_title = "YouTube Video Downloader"
page_icon = "▶️"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered")

st.image('YT_Downloader.jpg')
# Setup title and description
st.title(page_title)
st.write("Easy and most convenient way to download YouTube videos.")

# Main application functionality
st.subheader("YouTube Video URL:")
video_url = st.text_input("Enter the URL", placeholder="Enter the YT video URL", label_visibility="collapsed")
video_quality = st.selectbox("Select the Video Quality", ["Low", "High"], disabled=not video_url)
load_video = st.button('Load Video', type="primary", disabled=not video_url)
if load_video:
    with st.spinner(':blue[Retrieving Details. Please wait ...]'):
        get_youtube_videos_details(video_url, video_quality)
        st.success("Video loaded successfully!")

# ---- NAVIGATION MENU -----
selection = option_menu(
    menu_title=None,
    options=["Video Details", "Download", "About"],
    icons=["bi-youtube", "bi-cloud-arrow-down-fill", "", "app"],  # https://icons.getbootstrap.com
    orientation="horizontal",
)

# If selection is "Video Detail"
if selection == "Video Details":
    try:
        tmp = st.session_state.yt_df  # Accessing to check if video has been loaded or not
        st.subheader("Video Details")
        st.data_editor(st.session_state.yt_df, hide_index=True, use_container_width=True)
        st.subheader('Video Thumbnail')
        st.image(st.session_state.yt_thumbnail, width=400)
    except AttributeError:
        st.warning("Load Video by entering the URL and clicking on :blue[***Load Video***] button.")

# If selection is "Download"
if selection == "Download":
    try:
        title = st.session_state.yt_stream.title
        file_size = st.session_state.yt_stream.filesize_mb
        st.subheader('Download Video')
        st.write(f"Video Title: **:green[{title}]**")
        st.write(f"Video Size: {file_size:.1f} MB")
        # video_contents = download_youtube_videos(st.session_state.yt_stream)
        st.download_button('Download Video', type="primary",
                           data=st.session_state.video_contents,
                           file_name="yt_video.mp4")
    except AttributeError:
        st.warning("Load Video by entering the URL and clicking on :blue[***Load Video***] button.")

# If selection is "About"
if selection == "About":
    with st.expander("About this App"):
        st.markdown(''' This app allows you to download videos from YouTube. It has following functionality:

    - Allows to download video in high or low quality format
    - Display video detail like Channel Name, Video Title, Length and Views
        ''')
    with st.expander("Where to get the source code of this app?"):
        st.markdown(''' Source code is available at:
    *  https://github.com/mzeeshanaltaf/streamlit-yt-video-downloader
        ''')
    with st.expander("Whom to contact regarding this app?"):
        st.markdown(''' Contact [Zeeshan Altaf](zeeshan.altaf@gmail.com)
        ''')
