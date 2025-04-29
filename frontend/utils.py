import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Adresse du backend en local
# BACKEND_URL = "http://backend:8000"



def get_movie_by_id(movie_id):
    """Retourne les détails d’un film via l’API backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/movie/{movie_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Code {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


def get_recommendations(user_id):
    """Retourne une liste de recommandations pour un utilisateur via POST"""
    try:
        response = requests.post(f"{BACKEND_URL}/recommend_movies/{user_id}")
        if response.status_code == 200:
            data = response.json()
            return data.get("recommendations", [])
        else:
            return [{"error": f"Code {response.status_code}"}]
    except Exception as e:
        return [{"error": str(e)}]


def get_genre_distribution():
    """Retourne la distribution des genres de films"""
    try:
        response = requests.get(f"{BACKEND_URL}/statistics/genres_distribution")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except:
        return []


def get_films_per_year():
    """Retourne le nombre de films par année"""
    try:
        response = requests.get(f"{BACKEND_URL}/statistics/films_per_year")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except:
        return []
