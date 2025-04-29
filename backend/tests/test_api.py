import sys
import os

# Ajouter le dossier parent (backend) au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_movie():
    response = client.get("/movie/1197306")  # ID réel existant
    print(">> Movie:", response.status_code, response.text)
    assert response.status_code in [200, 404]

def test_recommend_movies():
    response = client.post("/recommend_movies/183007")  # Un user_id réel
    print(">> Reco:", response.status_code, response.text)
    assert response.status_code == 200
    assert "recommendations" in response.json()

def test_stats_genres():
    response = client.get("/statistics/genres_distribution")
    print(">> Genres:", response.status_code, response.text)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_stats_years():
    response = client.get("/statistics/films_per_year")
    print(">> Years:", response.status_code, response.text)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
