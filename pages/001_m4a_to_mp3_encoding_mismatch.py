import streamlit as st
import os

css_file = os.path.join("src", "styling.css") 

def create_info_card(title, content):
    """Create an info card with styled content"""
    card_html = f"""
    <div style='
        background-color: rgba(26, 26, 46, 0.8);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 204, 0, 0.2);
    '>
        <h3 style='
            font-family: Montserrat, sans-serif;
            color: #ffcc00;
            font-size: 1.6rem;
            margin: 0 0 1rem 0;
        '>{title}</h3>
        <div style='font-family: "Fira Code", monospace; color: #e0e0e0;'>
            {content}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# Set page config
st.set_page_config(page_title=".m4a to .mp3 converter", page_icon="🎵", layout="wide")
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1a1a2e, #D2C0DA) !important;
    background-attachment: fixed !important;
    min-height: 100vh;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='font-family: Montserrat, sans-serif; color: #ffcc00; font-size: 3.75rem; margin-bottom: 0.5rem; letter-spacing: 0.05em;'>.m4a to .mp3 encoding mismatch</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h2 style='font-family: Montserrat, sans-serif; color: #ffffff; font-size: 1.8em; margin-top: 1.5em;'>Background</h2>",
    unsafe_allow_html=True
)

st.markdown("""
    <div style="font-family: 'Fira Code', monospace; margin-bottom: 1em;">
        <span style="color: #ffcc00; font-weight: 700; font-size: 1.1em;">tl;dr:</span>
        <span style="color: #e0e0e0;"> An Apple Music beta feature released in 2015-2016 claimed to convert audio files to .m4a for simple integration with the Streaming files. Instead, it corrupted my audio files and I could not listen to these songs on my iPhone/ with  update from around  made some MP3 files incompatible..</span>
    </div>
    """, unsafe_allow_html=True)

# Expander with themed content
with st.expander(label="Long Story", expanded=False):
    st.markdown("""
    <div style="font-family: 'Fira Code', monospace; color: #e0e0e0; line-height: 1.6;">
        Back when iTunes was the go-to for audio file management and Limewire (RIP) was the norm, I had around 50 GB of music from 
        burned CDs and "other sources" (hopefully the Statute of Limitations is up on this). Apple Music came along, 
        introducing streaming music and simplifying music library management. Initially, Apple Music offered an option 
        to convert MP3 files to M4A files, which worked great in the beta version. However, the next update broke this 
        functionality, rendering my files incompatible with Apple Music (affected about 2GBs of audio files). To be conspiratorial, this 
        issue occurred around the same time Batterygate happened. For those who dont know, Apple purposefully reduced battery life 
        on older iPhone models with new software updates.) This issue f
        occurred around 2015-2016, 
         I've been gradually re-downloading my music files as I discovered they're no 
        longer compatible. I searched for free tools online that would do this and came up short, so this is my long
        overdue solution to recovering these files.
    </div>
    """, unsafe_allow_html=True) 

# Project Details section in a card
project_details_content = """
<ul style='list-style: none; padding-left: 0;'>
    <li style='margin-bottom: 0.8rem;'><span style='color: #ffcc00;'>▪</span> <strong>Project Goal:</strong> Recursively search for corrupted M4A files, list them in a text file, and then revert them back to MP3 format.</li>
    <li style='margin-bottom: 0.8rem;'><span style='color: #ffcc00;'>▪</span> <strong>Issue Description:</strong> Apple Music update around 2015-2016 made previously converted M4A files unreadable.</li>
    <li style='margin-bottom: 0.8rem;'><span style='color: #ffcc00;'>▪</span> <strong>Initial Music Library Size:</strong> Approximately 50 GB of music files.</li> 
</ul>
"""

# Create the Project Details card
create_info_card("Project Details", project_details_content)

# Divider to match about page style
st.divider()

# Footer with matching theme
st.markdown(
    "<p style='font-family: \"Fira Code\", monospace; color: #9fe2bf; font-size: 0.9em; margin-top: 2em; text-align: center;'>© 2025 Daniel Belay. All rights reserved.</p>",
    unsafe_allow_html=True
)