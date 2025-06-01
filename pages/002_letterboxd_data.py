import streamlit as st
import requests
import feedparser
import pandas as pd
import glob
import os
from functools import lru_cache
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
        st.error(f"TMDb API Error: {e}")
        return None

################################################### CSV FUNCTIONS #########################################################

@st.cache_data(ttl=3600)  # Cache TMDb API calls for 1 hour
def get_tmdb_movie_data_cached(movie_title, movie_year, api_key):
    """Enhanced TMDb API call with year for better disambiguation and caching"""
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": movie_title,
    }
    if movie_year and str(movie_year).isdigit():
        params["year"] = movie_year
        
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  
        data = response.json()
        if data and data.get("results"):
            return data["results"][0]
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"TMDb API Error: {e}")
        return None

def load_csv_files(csv_directory="assets/lttrbox_csvs"):
    """Load all CSV files from the letterboxd directory"""
    csv_files = {}
    csv_pattern = os.path.join(csv_directory, "*.csv")
    
    for csv_file in glob.glob(csv_pattern):
        filename = os.path.basename(csv_file)
        try:
            df = pd.read_csv(csv_file)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date', ascending=False)
            csv_files[filename] = df
        except Exception as e:
            st.error(f"Error loading {filename}: {e}")
    
    return csv_files

def display_movie_card(movie, tmdb_api_key):
    """Display a single movie card with TMDb data in compact format"""
    movie_name = movie.get('Name', 'Unknown Title')
    movie_year = movie.get('Year', '')
    letterboxd_uri = movie.get('Letterboxd URI', '#')
    rating = movie.get('Rating', '')
    
    tmdb_data = get_tmdb_movie_data_cached(movie_name, movie_year, tmdb_api_key)
    
    movie_content = {}
    
    if rating:
        movie_content["My Rating"] = f"★ {rating}/5"
    
    if tmdb_data:
        movie_content["Release"] = tmdb_data.get("release_date", "Unknown")
        overview = tmdb_data.get("overview", "")
        if overview:
            movie_content["Overview"] = overview[:80] + "..." if len(overview) > 80 else overview
        if tmdb_data.get("vote_average"):
            movie_content["TMDb"] = f"{tmdb_data.get('vote_average'):.1f}/10"
    
    movie_content["Letterboxd"] = f"<a href='{letterboxd_uri}' target='_blank' style='color: #87cefa;'>View</a>"
    
    title_display = f"{movie_name} ({movie_year})" if movie_year else movie_name
    create_info_card(title_display, movie_content)
    
    if tmdb_data and tmdb_data.get('poster_path'):
        st.image(f"https://image.tmdb.org/t/p/w300{tmdb_data.get('poster_path')}", use_container_width=True)

def display_selected_csv_movies(selected_df, dataset_name, tmdb_api_key):
    """Display movies from the selected CSV file in 4-column layout"""
    
    st.markdown(create_section_heading(f"{dataset_name} ({len(selected_df)} movies)"), unsafe_allow_html=True)
    
    movies_per_row = 4
    total_movies = len(selected_df)
    
    for row_start in range(0, total_movies, movies_per_row):
        row_end = min(row_start + movies_per_row, total_movies)
        cols = st.columns(movies_per_row)
        
        for i, (_, movie) in enumerate(selected_df.iloc[row_start:row_end].iterrows()):
            with cols[i]:
                display_movie_card(movie, tmdb_api_key)

################################################### MAIN APP CONTENT #########################################################

st.markdown(
    "<h1 style='font-family: Montserrat, sans-serif; color: #ffcc00; font-size: 3.75rem; margin-bottom: 0.5rem; letter-spacing: 0.05em;'>Letterboxd Movie Diary</h1>",
    unsafe_allow_html=True
)

################################################### INTRO #########################################################
intro_content = {
    "tl;dr": "Syncing my Letterboxd '/movie diary/' with The Movie Database (TMDb) to display my watch history and ratings with additional movie information.",
    None: "This page fetches my recent movie watches from Letterboxd's RSS feed and enhances each entry with data from TMDb's API.",
    None: "During this process I realized how bad the Letterboxd developer experience is. I am guessing its because (1)they are a small team and focused on the product, not the developer experience. And (2) there is some legal issue with exporting movie data.",
}
create_info_card("About the project", intro_content)

################################################### API KEY SETUP #########################################################
tmdb_api_key = os.getenv("TMDB_API_KEY")
if not tmdb_api_key:
    st.error("TMDb API key not configured. Daniel needs to check this out")
    st.stop()

################################################### RSS FEED SECTION #########################################################
letterboxd_rss_url = "https://letterboxd.com/dbtwothree/rss/"
letterboxd_entries = get_letterboxd_data(letterboxd_rss_url)

if letterboxd_entries:
    st.markdown(create_section_heading("Recent Watches (RSS Feed)"), unsafe_allow_html=True)
    
    movies_per_row = 4
    total_entries = len(letterboxd_entries)
    
    for row_start in range(0, total_entries, movies_per_row):
        row_end = min(row_start + movies_per_row, total_entries)
        cols = st.columns(movies_per_row)
        
        for i, entry in enumerate(letterboxd_entries[row_start:row_end]):
            with cols[i]:
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

################################################### CSV DATA SECTION #########################################################

if tmdb_api_key:  # Only load CSV data if we have TMDb API key
    st.markdown(create_section_heading("My Movie Collection from CSV Data"), unsafe_allow_html=True)
    
    dataset_explanations = {
        "watched.csv": "A list of all films you have marked as Watched. Dates correspond to when you watched them (chronological watch history).",
        "ratings.csv": "A list of all films you have rated on Letterboxd. Includes ratings without necessarily having a public review.",
        "films.csv": "A complete list of all your watched films. Similar to watched.csv but often includes rewatched titles or titles without logs (superset of your watches).",
        "watchlist.csv": "All films in your Watchlist. These are your planned watches, not actual viewings - films not yet marked as watched or rated."
    }
    
    explanation_content = {
        "Watch History (watched.csv)": dataset_explanations["watched.csv"],
        "Ratings (ratings.csv)": dataset_explanations["ratings.csv"], 
        "Full Film Log (films.csv)": dataset_explanations["films.csv"],
        "Watchlist (watchlist.csv)": dataset_explanations["watchlist.csv"],
        None: "Note: films.csv is a superset of your watches, watched.csv focuses on logged watches where date matters, ratings.csv may include ratings without reviews, and watchlist.csv is independent of actual viewings."
    }
    create_info_card("Dataset Explanations", explanation_content)
    
    csv_files = load_csv_files("assets/lttrbox_csvs")
    
    if csv_files:
        csv_display_options = {
            "Watch History": "watched.csv",
            "Ratings": "ratings.csv", 
            "Full Film Log": "films.csv",
            "Watchlist": "watchlist.csv"
        }
        
        selected_option = st.selectbox(
            "Select a movie dataset to view:",
            options=["Please select a movie data set"] + list(csv_display_options.keys()),
            index=0
        )
        
        if selected_option != "Please select a movie data set":
            selected_csv_file = csv_display_options[selected_option]
            
            if selected_csv_file in csv_files:
                selected_df = csv_files[selected_csv_file]
                display_selected_csv_movies(selected_df, selected_option, tmdb_api_key)
            else:
                st.warning(f"File {selected_csv_file} not found in the CSV directory.")
                
    else:
        no_csv_content = {
            "Status": "No CSV files found in assets/lttrbox_csvs/",
            None: "Make sure your CSV files are in the correct directory with the expected format."
        }
        create_info_card("No CSV Data Available", no_csv_content)

st.divider()
add_footer()