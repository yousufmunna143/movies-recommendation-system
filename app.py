import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c4c9897af1ecb7aa91be175d81e5694f&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w185/"+data['poster_path']
def fetch_rating(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c4c9897af1ecb7aa91be175d81e5694f&language=en-US'.format(movie_id))
    data = response.json()
    return data['vote_average']
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:6]
    recommended_movies = []
    movie_ratings = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch posters from API
        recommended_movies_posters.append(fetch_poster(movie_id))
        movie_ratings.append((fetch_rating(movie_id)))
    return recommended_movies,recommended_movies_posters,movie_ratings

st.title('movie recommender system')


selected_movie_name = st.selectbox(
   "Select your favourite movie",
   movies['title'].values,
   index=None,
)



if st.button('Recommend'):
    names,posters,rating = recommend(selected_movie_name)
    st.write('Movies you may also like:')

    col1, col2, col3, col4, col5= st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
        st.text("Rating:" + str(rating[0]))

    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.text("Rating:" + str(rating[1]))

    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.text("Rating:" + str(rating[2]))

    with col4:
        st.text(names[3])
        st.image(posters[3])
        st.text("Rating:" + str(rating[3]))

    with col5:
        st.text(names[4])
        st.image(posters[4])
        st.text("Rating:" + str(rating[4]))