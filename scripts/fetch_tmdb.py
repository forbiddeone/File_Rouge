import requests
import json
import time
import pandas as pd
import os

API_KEY = "1e06b843c3b8e6ce9c3d3da54a708cd4"
BASE_URL = "https://api.themoviedb.org/3"
OUTPUT_PATH = "data/raw/tmdb_movies.csv"

def get_genre_mapping():
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    genres = response.json()["genres"]
    return {genre["id"]: genre["name"] for genre in genres}

def fetch_movies(pages=500):
    all_movies = []
    for page in range(1, pages + 1):
        print(f"Récupération page {page}/{pages}...")
        url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&language=en-US&sort_by=popularity.desc&vote_count.gte=50&page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            all_movies.extend(data["results"])
        else:
            print(f"Erreur page {page} : {response.status_code}")
            break
        time.sleep(0.25)  # Pause pour éviter d'abuser de l'API
    return all_movies

def clean_movies_data(movies, genre_mapping):
    return pd.DataFrame([
        {
            "id": movie["id"],
            "title": movie["title"],
            "genres": json.dumps([genre_mapping.get(gid, "Unknown") for gid in movie.get("genre_ids", [])]),
            "description": movie.get("overview", ""),
            "release_date": movie.get("release_date", ""),
            "vote_average": movie.get("vote_average", None),
            "vote_count": movie.get("vote_count", None)
        } for movie in movies if movie.get("vote_count", 0) >= 50
    ])

def main():
    os.makedirs("data/raw", exist_ok=True)

    print("Récupération des genres...")
    genre_mapping = get_genre_mapping()

    print("Récupération des films depuis TMDB...")
    movies = fetch_movies(pages=500)

    print(f"Nombre total de films récupérés : {len(movies)}")

    df = clean_movies_data(movies, genre_mapping)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Fichier enregistré : {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
