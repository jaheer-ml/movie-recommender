import pickle
import streamlit as st
import requests
import pandas as pd
import time
import gdown
import os

# Local filenames
movies_path = "movies_dict.pkl"
similarity_path = "similarity.pkl"

# Google Drive direct download links using file IDs
movies_url = "https://drive.google.com/uc?id=1D9K9KqDydqAzCVV_JqaJBySNUqjG2LFD"
similarity_url = "https://drive.google.com/uc?id=1R9jFNzU1pN448hrcFhzqpuU9HLfFbFUy"

# Download files only if they don't exist locally
if not os.path.exists(movies_path):
    gdown.download(movies_url, movies_path, quiet=False, fuzzy=True)

if not os.path.exists(similarity_path):
    gdown.download(similarity_url, similarity_path, quiet=False, fuzzy=True)

# Load the downloaded files
with open("movies_dict.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)
    
# ------------------ Fetch poster ------------------ #
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d7840b9543b6275389db4077192f2aee&language=en-US"
    try:
        data = requests.get(url, timeout=10).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Image"

# ------------------ Recommendation logic ------------------ #
def recommend(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []

    for i in distances[1:5]:
        movie_id = movies_df.iloc[i[0]]['id']
        recommended_movie_ids.append(movie_id)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies_df.iloc[i[0]]['title'])

    return recommended_movie_names, recommended_movie_posters, recommended_movie_ids

# ------------------ Streamlit UI ------------------ #


st.set_page_config(page_title="Movie Recommender", layout="wide")

# Background & CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: rgba(0,0,0,0.8);
    }

    /* Modern title style */
    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        background: linear-gradient(90deg, #FF4B4B, #FF8C42);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 12px rgba(255,75,75,0.5);
        margin-bottom: 10px;
    }

    .movie-card {
        position: relative;
        text-align: center;
        color: white;
        font-weight: bold;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        transition: all 0.4s ease-in-out;
        border: 2px solid transparent;
        backdrop-filter: blur(8px);
        background: rgba(255,255,255,0.05);
        animation: fadeIn 0.6s ease-in-out;
    }

    .movie-card img {
        width: 100%;
        border-radius: 16px;
        transition: all 0.3s ease-in-out;
    }

    .movie-card:hover {
        transform: translateY(-8px) scale(1.03) rotate3d(1,1,0,2deg);
        box-shadow: 0 12px 25px rgba(255,75,75,0.6);
        border: 2px solid #FF4B4B;
    }

    .movie-card img:hover {
        transform: scale(1.05);
        filter: brightness(1.1);
    }

    .movie-title {
        background: rgba(0,0,0,0.6);
        padding: 8px 0;
        position: absolute;
        bottom: 0;
        width: 100%;
        font-size: 16px;
        text-shadow: 0px 0px 8px rgba(255,75,75,0.8);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["App", "Code"]) 

with tab1:

    # Title
    st.markdown("<h1 class='main-title'>🎬 Recommender System - MovieFLIX</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border:2px solid #FF4B4B; margin-bottom:30px;'>", unsafe_allow_html=True)
    
    # Load pickled data
    movies_df = pd.DataFrame(movies)

    # Movie dropdown
    selected_movie = st.selectbox("Type or select a movie", movies_df['title'].values, index=0)

    # Show recommendations
    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters, recommended_movie_ids = recommend(selected_movie)

        cols = st.columns(4)
        for col, name, poster, movie_id in zip(cols, recommended_movie_names, recommended_movie_posters, recommended_movie_ids):
            with col:
                tmdb_url = f"https://www.themoviedb.org/movie/{movie_id}"
                col.markdown(f"""
                    <div class="movie-card">
                        <a href="{tmdb_url}" target="_blank">
                            <img src="{poster}">
                        </a>
                        <div class="movie-title">{name}</div>
                    </div>
                """, unsafe_allow_html=True)
                time.sleep(1)

with tab2:

    # Password check only for code tab
    st.subheader("App Logic / Code")
    password = st.text_input("Enter password to view code:", type="password")
    if password == "jbmlprojects":
        code = """
import pickle
import streamlit as st
import requests
import pandas as pd

# ------------------ Fetch poster ------------------ #
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d7840b9543b6275389db4077192f2aee&language=en-US"
    try:
        data = requests.get(url, timeout=10).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=No+Image"

# ------------------ Recommendation logic ------------------ #
def recommend(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []

    for i in distances[1:5]:
        movie_id = movies_df.iloc[i[0]]['id']
        recommended_movie_ids.append(movie_id)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies_df.iloc[i[0]]['title'])

    return recommended_movie_names, recommended_movie_posters, recommended_movie_ids

# ------------------ Streamlit UI ------------------ #
st.title("🎬 Movie Recommender System")

movies = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_df = pd.DataFrame(movies)

selected_movie = st.selectbox("Type or select a movie", movies_df['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_ids = recommend(selected_movie)

    cols = st.columns(4)
    for col, name, poster, movie_id in zip(cols, recommended_movie_names, recommended_movie_posters, recommended_movie_ids):
        with col:
            tmdb_url = f"https://www.themoviedb.org/movie/{movie_id}"
            st.image(poster, caption=name)
            st.markdown(f"[More info]({tmdb_url})")
"""
        st.code(code, language="python")
    elif password:
        st.warning("Incorrect password! Access denied.")
