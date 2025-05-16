import streamlit as st
import requests
import feedparser
import os
from src.st_server_utils import create_navigation
from src import env_utils 
from src.text_utils import create_info_card, add_footer, create_section_heading

################################################### PAGE SETTINGS  #########################################################
st.set_page_config(
    page_title="Letterboxd Data", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded",
)
create_navigation()
css_file = os.path.join("assets", "styling.css")
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

################################################### RSS FUNCTIONS #########################################################
def get_letterboxd_data(rss_url):
    """No clue why, but Letterboxd doesnt have an API, so im using the RSS feed. I regret this project, but Im in too deep"""
    try:
        feed = feedparser.parse(rss_url)
        return feed.entries
    except Exception as e:
        st.error(f"Error fetching or parsing RSS feed: {e}")
        return []

def get_tmdb_movie_data(movie_title, api_key):
    """Letterboxd RSS Feed sux, so im using the movie title to search TMDb's free API to get movie data."""
    # """structure of the request: (1) static url+ (2) api_key+ (3) query"""
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": movie_title,
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  
        data = response.json()
        if data and data.get("results"):
            return data["results"][0]
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from TMDb: {e}")
        return None

st.markdown(
    "<h1 style='font-family: Montserrat, sans-serif; color: #ffcc00; font-size: 3.75rem; margin-bottom: 0.5rem; letter-spacing: 0.05em;'>Letterboxd Movie Diary</h1>",
    unsafe_allow_html=True
)
################################################### INTRO #########################################################
intro_content = {
    "tl;dr": "Syncing my Letterboxd '/movie diary/' with The Movie Database (TMDb) to display my watch history and ratings with additional movie information.",
    None: "This page fetches my recent movie watches from Letterboxd's RSS feed and enhances each entry with data from TMDb's API.",
    None: "During this process I realized how bad the Letterboxd developer experience is. I am guessing its because (1)they are a small team and focused on the product, not the developer experience. And (2) there is some legal issue with exporting movie data.",
    # None: "Here are some solutions others have made:",
    # None: "– Obsidena",
    # None: "     – https://www.obsidianstats.com/plugins/letterboxd-rss-sync ",
}
create_info_card("About the project", intro_content)
tmdb_api_key = os.getenv("TMDB_API_KEY")
if not tmdb_api_key:
    api_key_content = {
        "Action Required": "TMDb API key not found in environment variables. Please enter your key below.",
        None: "You can get a free API key from The Movie Database (TMDb) by creating an account at themoviedb.org."
    }
    create_info_card("API Key Missing", api_key_content)
    with st.expander("Debug Information", expanded=False):
        st.code(f"Current working directory: {os.getcwd()}")
        st.code(f"Environment variable exists: {'TMDB_API_KEY' in os.environ}")
        st.code(f".env file exists: {os.path.exists(os.path.join(os.getcwd(), '.env'))}")
    
    tmdb_api_key = st.text_input("Enter your TMDb API Key:", type="password")
    if tmdb_api_key:
        st.success("API key entered. You can save this in your .env file for future use.")
    else:
        st.error("Please enter a valid TMDb API key to continue.")
        st.stop()

letterboxd_rss_url = "https://letterboxd.com/dbtwothree/rss/"
letterboxd_entries = get_letterboxd_data(letterboxd_rss_url)

if letterboxd_entries:
    st.markdown(create_section_heading("Recent Watches"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    for i, entry in enumerate(letterboxd_entries):
        current_col = col1 if i % 2 == 0 else col2
        with current_col:
            title = entry.get("title", "No Title")
            link = entry.get("link", "#")
            published = entry.get("published", "No Date")
            summary = entry.get("summary", "No Summary")
            movie_title_for_tmdb = title.split(" by ")[0].strip()
            tmdb_data = get_tmdb_movie_data(movie_title_for_tmdb, tmdb_api_key)
            movie_content = {}
            movie_content["Letterboxd Review"] = f"<a href='{link}' target='_blank' style='color: #87cefa;'>Read my review</a>"
            movie_content["Review Date"] = published
            if "★" in summary:
                movie_content["My Rating"] = summary.split("<p>")[0] if "<p>" in summary else summary
            if "<p>" in summary:
                clean_summary = summary.split("<p>")[1].split("</p>")[0]
                movie_content["My Review"] = clean_summary
            if tmdb_data:
                movie_content["Release Date"] = tmdb_data.get("release_date", "Unknown")
                movie_content["Overview"] = tmdb_data.get("overview", "No overview available")
                if tmdb_data.get("vote_average"):
                    movie_content["TMDb Rating"] = f"{tmdb_data.get('vote_average')}/10 ({tmdb_data.get('vote_count', 0)} votes)"
                create_info_card(movie_title_for_tmdb, movie_content)
                poster_path = tmdb_data.get('poster_path')
                if poster_path:
                    st.image(f"https://image.tmdb.org/t/p/w500{poster_path}", width=300)
            else:
                create_info_card(movie_title_for_tmdb, movie_content)
else:
    no_data_content = {
        "Status": "No Letterboxd entries found.",
        None: "Check your Letterboxd RSS URL or try again later."
    }
    create_info_card("No Data Available", no_data_content)

st.divider()
add_footer()