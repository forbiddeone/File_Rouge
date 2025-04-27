import pytest
from unittest.mock import patch
import streamlit as st
from utils import get_movie_by_id, get_recommendations, get_genre_distribution, get_films_per_year

# Mock de Streamlit pour ne pas vraiment exécuter l'affichage
@pytest.fixture(autouse=True)
def no_streamlit_render(monkeypatch):
    monkeypatch.setattr(st, "set_page_config", lambda *args, **kwargs: None)
    monkeypatch.setattr(st, "title", lambda *args, **kwargs: None)
    monkeypatch.setattr(st, "expander", lambda *args, **kwargs: DummyContextManager())
    monkeypatch.setattr(st, "number_input", lambda *args, **kwargs: 1)
    monkeypatch.setattr(st, "button", lambda *args, **kwargs: True)
    monkeypatch.setattr(st, "success", lambda *args, **kwargs: None)
    monkeypatch.setattr(st, "write", lambda *args, **kwargs: None)
    monkeypatch.setattr(st, "warning", lambda *args, **kwargs: None)
    monkeypatch.setattr(st, "markdown", lambda *args, **kwargs: None)
    monkeypatch.setattr(st, "subheader", lambda *args, **kwargs: None)
    monkeypatch.setattr(st, "plotly_chart", lambda *args, **kwargs: None)

class DummyContextManager:
    def __enter__(self): return self
    def __exit__(self, *args): pass


# --- Tests de utils (backend communication) ---

def test_get_movie_by_id_success():
    with patch('utils.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"title": "Fight Club", "year": 1999}
        
        movie = get_movie_by_id(550)
        assert movie["title"] == "Fight Club"
        assert movie["year"] == 1999

def test_get_movie_by_id_failure():
    with patch('utils.requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        
        movie = get_movie_by_id(9999)
        assert "error" in movie


def test_get_recommendations_success():
    with patch('utils.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "recommendations": [{"title": "Inception", "rating_predicted": 4.5}]
        }
        
        recos = get_recommendations(1)
        assert isinstance(recos, list)
        assert recos[0]["title"] == "Inception"

def test_get_genre_distribution_success():
    with patch('utils.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"genre": "Action", "count": 50}]
        
        genres = get_genre_distribution()
        assert genres[0]["genre"] == "Action"

def test_get_films_per_year_success():
    with patch('utils.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"year": 1999, "count": 20}]
        
        years = get_films_per_year()
        assert years[0]["year"] == 1999
