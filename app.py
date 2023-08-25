import streamlit as st
import requests
import pandas as pd
import pickle


def fetch_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


def fetch_release_year(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return data["release_date"].split("-")[0]  # Extract year from release date


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_years = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]]["movie_id"]
        recommended_movies.append(movies.iloc[i[0]]["title"])
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_years.append(fetch_release_year(movie_id))
    return recommended_movies, recommended_movies_posters, recommended_movies_years


# Load movies and similarity data
movies_list = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movies Recommender System")

movies_list = movies_list["title"].values

option = st.selectbox(
    "Select a Movie",
    movies_list
)

if st.button("Recommend"):
    names, posters, years = recommend(option)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.write(names[0])
        st.write("Year:", years[0])
    
    with col2:
        st.image(posters[1])
        st.write(names[1])
        st.write("Year:", years[1])
    
    with col3:
        st.image(posters[2])
        st.write(names[2])
        st.write("Year:", years[2])
    
    with col4:
        st.image(posters[3])
        st.write(names[3])
        st.write("Year:", years[3])
    
    with col5:
        st.image(posters[4])
        st.write(names[4])
        st.write("Year:", years[4])
