
import numpy as np
import json
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
def getRef(movies_data,movie_name):
    selected_features = ['genres','keywords','original_title','production_companies','spoken_languages','tagline','cast','director']
    for feature in selected_features:
        movies_data[feature] = movies_data[feature].fillna('')
    combined_features = movies_data['genres'] + movies_data['keywords']+ movies_data['original_title']\
                        +movies_data['tagline']\
                        +movies_data['cast'] + movies_data['production_companies'] + movies_data['spoken_languages'] \
                        + movies_data['director']
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)

    list_of_all_titles = movies_data['original_title'].tolist()

    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    close_match = find_close_match[0]

    index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]

    similarity_score = list(enumerate(similarity[index_of_the_movie]))

    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    json_movie = {}
    i = 1
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movies_data[movies_data.index == index]['original_title'].to_string()
        if i < 10:
            json_movie.setdefault(title_from_index)
            i += 1
    newSet = tuple(json_movie)
    json_str = json.dumps(newSet)
    return json_str
