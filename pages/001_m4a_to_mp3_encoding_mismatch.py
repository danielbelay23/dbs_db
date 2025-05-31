import streamlit as st
import os
from src.text_utils import create_info_card, add_footer
from src.st_server_utils import create_navigation
# from src.viz_utils import nodes, edges, streamlit_flow, StreamlitFlowState

st.set_page_config(
    page_title=".m4a to .mp3 converter", 
    page_icon="🎵", 
    layout="wide",
    initial_sidebar_state="expanded",
)
create_navigation()
css_file = os.path.join("assets", "styling.css")

# if os.path.exists(flow_diagram_file):
#     with open(flow_diagram_file, "r") as f:
#         flow_diagram_code = f.read()
#     flow_diagram_code

if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
 
st.markdown(
    "<h1 style='font-family: Montserrat, sans-serif; color: #ffcc00; font-size: 3.75rem; margin-bottom: 0.5rem; letter-spacing: 0.05em;'>.m4a to .mp3 codec mismatch</h1>",
    unsafe_allow_html=True
)
######################################################### PROBLEM #########################################################
problem_content = {
    "tl;dr": "An Apple Music beta feature released in 2015-2016 claimed to convert audio files to .m4a for simple integration with the Streaming files. Instead, it corrupted my audio files and I could not listen to these songs on my iPhone/ with update from around 2015-2016 made some MP3 files incompatible.",
}
create_info_card("Problem", problem_content)
with st.expander(label="Long Story", expanded=False):
    st.markdown("""
    <div style="font-family: 'Montserrat', sans-serif; color: #e0e0e0; line-height: 1.6; ">
        Remember when iTunes was the go-to for managing music files and Limewire (RIP) was the norm? I had around 50 GB of music from burned CDs and other sources (hopefully the statute of limitations is up on that). Apple Music came along and introduced streaming music and made it easier to manage my music library. At first, Apple Music had an option to convert MP3 files to M4A files, which worked great in the beta version. But then, the next update broke this functionality, making ~2GBs of prime Weezy F. Baby, Dipset, and Blink 182 incompatible with Apple Music.
        <br><br>
        To be conspiratorial, this issue occurred around the time of Batterygate (when Apple purposefully reduced battery life on older iPhone models with new software updates). Also, when I was using Apple Intelligence for proofreading this paragraph, it rewrote this section as
        "I've heard that Apple accidentally reduced battery life on older iPhone models with new software updates and later corrected it."
        <br><br>
        Anyway, I've been gradually re-downloading my music files as I discovered they're no longer compatible. I searched for free tools online that would do this and came up short, so this is my long-overdue solution to recovering these files.
    </div>
    """, unsafe_allow_html=True 
)
######################################################### CONTEXT #########################################################
context_content = {
    "tl;dr": "My files were encoded with mp3 codec, but Apple Music thought they were m4a files because the file extension and container was .m4a.",
    None: "A codec (short for Coder-Decoder) is the algorithm that compresses and decompresses audio data (e.g. MP3 or AAC). The file extension (container) like .m4a is just a label and doesn't guarantee which codec is inside—so an MP3‑encoded track can be mislabeled as .m4a. macOS's 'Get Info' shows the extension, not the actual codec.",
}

create_info_card("Context", context_content)

with st.expander(label="Long Story", expanded=False):
    st.markdown("""
    <div style="font-family: 'Montserrat', sans-serif; color: #e0e0e0; line-height: 1.6;">
        The core issue was that my audio files had their codecs incorrectly labeled with an <code>.m4a</code> file extension (their container). After an Apple Music update, the software started trusting the <code>.m4a</code> label more strictly, leading to a mismatch because it expected AAC-encoded content (typical for <code>.m4a</code>) but found MP3 data instead. This made the files unplayable.
        <br><br>
        Understanding the difference between a <b>codec</b> and a <b>container</b> is key here. The image below illustrates the general encoding process:
    </div>
    """, unsafe_allow_html=True
    )

    st.image("assets/m4a/codec_diagram.png", caption="")

    st.markdown("""
    <div style="font-family: 'Montserrat', sans-serif; color: #e0e0e0; line-height: 1.6; margin-top: 1em; ">
        Essentially, the codec (like MP3 or AAC) is the recipe for compressing and decompressing the audio. The container (like <code>.m4a</code> or <code>.mp3</code>) is just the box it's stored in, and its label (the file extension) is just a hint.
        <br><br>
        As you can see in the macOS "Get Info" panel (example below), the system often displays information based on the file extension (the container's label) rather than deep-inspecting the actual codec of the audio stream within. So, even if the content was MP3, if the extension was <code>.m4a</code>, that's what "Get Info" would often reflect for the 'Kind' of file.
    </div>
    """, unsafe_allow_html=True)

    st.image("assets/m4a/example_get_info.png", caption="Example of macOS 'Get Info' panel")

st.info("""
        This issue is specific to macOS. Windows and Linux systems handle file extensions differently, so this problem doesn't occur on those platforms.
        """, 
        icon="ℹ️"
    )

st.divider() 
######################################################### PROJECT DETAILS #########################################################

project_details_content = {
    "Project Goal": "find, document and resolve mismatches between codec and container",
    "Steps": "(1) recursively search for corrupted M4A files in Music directory (2) list all files with mismatches in a txt file for QA (3) update container value to match codec.",
    "Solution": "For steps (1) and (2) use shell script + FFprobe to search and document. For step (3) use FFmpeg to convert the container to match codec format."
}

create_info_card("Project Details", project_details_content)
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
with st.expander(label="Usage Instructions", expanded=False):
    st.markdown(
        """ 
        <style>
        .usage-instructions code, .usage-instructions pre {
            background-color: #2a2a3a !important;
        }
        </style>

        <div class="usage-instructions">


        **Requirements**
        - Install ffmpeg & ffprobe via Homebrew:
        ```bash
        brew install ffmpeg
        ```

        **Steps**
        1. **Unzip** the downloaded `M4A Fix Toolkit` zip.
        2. **Open Terminal** and navigate:
        ```bash
        cd /path/to/unzipped/folder
        ```
        3. **Make scripts executable**: 
        ```bash
        chmod +x check_audio_files.sh rename_m4a_to_mp3.sh fix_mismatched_files.sh
        ```
        4. **Check mismatches**:
        ```bash
        ./check_audio_files.sh "/path/to/music/folder" "$HOME/Desktop/mismatches.txt"
        ```
        5. **Rename mislabeled files**:
        ```bash
        ./rename_m4a_to_mp3.sh "/path/to/music/folder" "$HOME/Desktop/renamed_files.log"
        ```
        6. **Fix encoding mismatches**:
        ```bash
        ./fix_mismatched_files.sh "$HOME/Desktop/mismatches.txt"
        ```
        </div>
    """, unsafe_allow_html=True)

st.divider()

add_footer()
