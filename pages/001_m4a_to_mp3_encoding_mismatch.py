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

instructions_content = {
    "Overview": "Copy each script block below into its own file, make them executable, and run in sequence.",
    "Requirements": "Ensure ffmpeg and ffprobe are installed via Homebrew: `brew install ffmpeg`",
    "Default paths": "Scripts default to ~/Music/Music/Media.localized/Music for input and ~/Desktop for output files if paths are omitted."
}

create_info_card("Quick Copy-Paste & Run Instructions", instructions_content)

with st.expander(label="Detailed Steps", expanded=False):
    st.markdown("""
    <div style="font-family: 'Montserrat', sans-serif; color: #e0e0e0; line-height: 1.6;">
        <strong style="color: #ffcc00;">1. Create the script files:</strong><br>
        Copy each script block below into its own file: <code>check_audio_files.sh</code>, <code>rename_m4a_to_mp3.sh</code>, and <code>fix_mismatched_files.sh</code>
        <br><br>
        <strong style="color: #ffcc00;">2. Navigate to script directory:</strong><br>
        <code>cd /path/to/your/scripts</code>
        <br><br>
        <strong style="color: #ffcc00;">3. Make scripts executable:</strong><br>
        <code>chmod +x check_audio_files.sh rename_m4a_to_mp3.sh fix_mismatched_files.sh</code>
        <br><br>
        <strong style="color: #ffcc00;">4. Run the scripts in order:</strong><br>
        <code>./check_audio_files.sh "/Users/you/Music/Music/Media.localized/Music" "$HOME/Desktop/mismatches.txt"</code><br>
        <code>./rename_m4a_to_mp3.sh "/Users/you/Music/Music/Media.localized/Music" "$HOME/Desktop/renamed_files.log"</code><br>
        <code>./fix_mismatched_files.sh "$HOME/Desktop/mismatches.txt"</code>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
.script-title {
    font-family: 'Montserrat', sans-serif;
    color: #ffcc00;
    font-size: 1.6rem;
    margin: 0 0 1rem 0;
    text-align: center;
    background-color: rgba(26, 26, 46, 0.8);
    border-radius: 10px 10px 0 0;
    padding: 1rem;
    border: 1px solid rgba(255, 204, 0, 0.2);
    border-bottom: none;
}
.stCodeBlock {
    background-color: #2a2a3a !important;
}
.stCodeBlock > div {
    background-color: #2a2a3a !important;
}
.stCodeBlock pre {
    background-color: #2a2a3a !important;
    border-radius: 0 0 10px 10px !important;
    border: 1px solid rgba(255, 204, 0, 0.2) !important;
    border-top: none !important;
}
.stCodeBlock code {
    background-color: #2a2a3a !important;
    color: #e0e0e0 !important;
    font-family: 'Fira Code', monospace !important;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<h3 class="script-title">check_audio_files.sh</h3>', unsafe_allow_html=True)
    st.code("""#!/usr/bin/env bash
#
# Usage:
#   ./check_audio_files.sh /path/to/music/dir /path/to/output.txt
#
# - MUSIC_DIR:   Directory where your music files live (default: ~/Music/Music/Media.localized/Music)
# - OUTPUT_FILE: File to write the list of codec-mismatched files (default: ~/Desktop/mismatched_files.txt)

MUSIC_DIR="${1:-$HOME/Music/Music/Media.localized/Music}"
OUTPUT_FILE="${2:-$HOME/Desktop/mismatched_files.txt}"

# Overwrite any existing output file
> "$OUTPUT_FILE"

# Iterate over all .m4a and .mp3 files
find "$MUSIC_DIR" -type f \\( -iname "*.m4a" -o -iname "*.mp3" \\) | while read -r file; do
    # Get the file extension in lowercase
    extension=$(echo "${file##*.}" | tr '[:upper:]' '[:lower:]')
    # Probe the actual codec inside the file
    codec=$(ffprobe -v error \\
        -show_entries stream=codec_name \\
        -of default=noprint_wrappers=1:nokey=1 "$file" 2>/dev/null | head -n 1)

    # Determine what codec we expect based on the extension
    if [[ "$extension" == "m4a" ]]; then
        expected_codec="aac"
    elif [[ "$extension" == "mp3" ]]; then
        expected_codec="mp3"
    else
        # Skip anything else
        continue
    fi

    # If the actual codec doesn't match our expectation, log it
    if [[ "$codec" != "$expected_codec" ]]; then
        echo "$file" >> "$OUTPUT_FILE"
    fi
done

echo "Completed. Mismatched files have been logged to: $OUTPUT_FILE" """, language="bash")

with col2:
    st.markdown('<h3 class="script-title">rename_m4a_to_mp3.sh</h3>', unsafe_allow_html=True)
    st.code("""#!/usr/bin/env bash
#
# Usage:
#   ./rename_m4a_to_mp3.sh /path/to/music/dir /path/to/log.txt
#
# - TARGET_DIR: Directory where your music files live (default: ~/Music/Music/Media.localized/Music)
# - LOG_FILE:   File to write a log of all renamed files (default: ~/Desktop/renamed_files.log)
#
# This script scans for any ".m4a" files that are actually MP3-encoded and renames them
# from "filename.m4a" → "filename.mp3." If a .mp3 file of that name already exists, it skips.

TARGET_DIR="${1:-$HOME/Music/Music/Media.localized/Music}"
LOG_FILE="${2:-$HOME/Desktop/renamed_files.log}"

# Overwrite any existing log file
> "$LOG_FILE"

# Find all .m4a files
find "$TARGET_DIR" -type f -iname "*.m4a" | while read -r file; do
    # Probe actual codec
    codec=$(ffprobe -v error \\
        -show_entries stream=codec_name \\
        -of default=noprint_wrappers=1:nokey=1 "$file" 2>/dev/null | head -n 1)

    # If the codec is MP3, rename the file to .mp3
    if [[ "$codec" == "mp3" ]]; then
        new_file="${file%.m4a}.mp3"
        if [[ -f "$new_file" ]]; then
            echo "Skipped (already exists): $new_file" | tee -a "$LOG_FILE"
        else
            mv "$file" "$new_file"
            echo "Renamed: $file → $new_file" | tee -a "$LOG_FILE"
        fi
    fi
done

echo "Renaming complete. See the log at: $LOG_FILE" """, language="bash")

with col3:
    st.markdown('<h3 class="script-title">fix_mismatched_files.sh</h3>', unsafe_allow_html=True)
    st.code("""#!/usr/bin/env bash
    #
    # Usage:
    #   ./fix_mismatched_files.sh /path/to/mismatched_files.txt
    #
    # This script reads a list of file paths (one per line) from the provided text file.
    # For each file, it re-encodes the audio into the correct format (AAC for .m4a or MP3 for .mp3),
    # then replaces the original file with the newly encoded version.

    MISMATCHED_FILE="${1:-$HOME/Desktop/mismatched_files.txt}"

    # Check that the input list exists
    if [[ ! -f "$MISMATCHED_FILE" ]]; then
        echo "Error: Mismatched file list not found at: $MISMATCHED_FILE"
        exit 1
    fi

    while IFS= read -r file; do
        # Skip empty lines
        [[ -z "$file" ]] && continue

        if [[ -f "$file" ]]; then
            extension=$(echo "${file##*.}" | tr '[:upper:]' '[:lower:]')
            codec=$(ffprobe -v error \\
                -show_entries stream=codec_name \\
                -of default=noprint_wrappers=1:nokey=1 "$file" 2>/dev/null | head -n 1)

            # Determine expected codec
            if [[ "$extension" == "m4a" ]]; then
                expected_codec="aac"
                ffmpeg_codec="aac"
            elif [[ "$extension" == "mp3" ]]; then
                expected_codec="mp3"
                ffmpeg_codec="libmp3lame"
            else
                # Skip any other extensions
                continue
            fi

            if [[ "$codec" != "$expected_codec" ]]; then
                echo "Fixing: $file  (expected: $expected_codec, got: $codec)"
                temp_file="${file}.tmp.$extension"
                ffmpeg -y -i "$file" -c:a "$ffmpeg_codec" -b:a 256k "$temp_file" < /dev/null

                if [[ -f "$temp_file" ]]; then
                    mv "$temp_file" "$file"
                    echo "Replaced: $file"
                else
                    echo "Failed to re-encode: $file"
                fi
            else
                echo "Already correct: $file"
            fi
        else
            echo "File not found (skipped): $file"
        fi
    done < "$MISMATCHED_FILE"

    echo "All mismatched files processed." """, language="bash")

add_footer()
