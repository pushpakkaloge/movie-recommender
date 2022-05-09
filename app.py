import streamlit as st
import pickle
import pandas as pd
import requests

#import similarity
similarity = pickle.load(open('similarity.pkl','rb'))

#import movies dictionary
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict);

def getPoster(movieId):
    response = requests.get('https://api.themoviedb.org/3/movie/'+str(movieId)+'?api_key=69ec28ab06d6821ce9381806adb66d29')
    data = response.json();
    return 'https://image.tmdb.org/t/p/w780/'+ str(data['poster_path']);

def recommend_movies(movie):
    final_movies_list = [];
    recommend_movies_posters =[];
    index = movies[movies['title'] == movie].index[0];
    sortedMoviesData = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6];

    # fetching movies according to their indexes
    for i in sortedMoviesData:
        #getting posters from movies id
        movie_id = movies.iloc[i[0]].movie_id;
        poster = getPoster(movie_id);
        recommend_movies_posters.append(poster);

        final_movies_list.append(movies.iloc[i[0]].title);
    return final_movies_list,recommend_movies_posters;





st.title('Movie Recommendation System')
selected_movie = st.selectbox('Select A movie From list',movies['title'].values)

if (st.button('Recommend')):
    recommendations,posters = recommend_movies(selected_movie);
    
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.text(recommendations[0]);

    with col2:
        st.image(posters[1])
        st.text(recommendations[1]);

    with col3:
        st.image(posters[2])
        st.text(recommendations[2]);

    with col4:
        st.image(posters[3])
        st.text(recommendations[3]);

    with col5:
        st.image(posters[4])
        st.text(recommendations[4]);
