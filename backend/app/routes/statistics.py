from fastapi import APIRouter, HTTPException
from app.database import con
import pandas as pd

router = APIRouter()

@router.get("/top_rated/{genre}/{year}")
def get_top_rated(genre: str, year: str):
    """Top 10 des films les mieux notés pour un genre et une année donnés"""
    try:
        query = """
        SELECT id, title, vote_average, release_date
        FROM films
        WHERE genres LIKE ?
        AND release_date LIKE ?
        ORDER BY vote_average DESC
        LIMIT 10;
        """
        results = con.execute(query, (f"%{genre}%", f"{year}%")).fetchall()
        return [
            {"id": r[0], "title": r[1], "rating": r[2], "release_date": r[3]}
            for r in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/genres_distribution")
def get_genre_distribution():
    """Retourne une liste des genres les plus fréquents"""
    try:
        query = "SELECT genres FROM films WHERE genres IS NOT NULL;"
        results = con.execute(query).fetchdf()

        df = results["genres"].str.split(",").explode().str.strip()
        genre_counts = df.value_counts().reset_index()
        genre_counts.columns = ["genre", "count"]
        return genre_counts.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/films_per_year")
def get_films_per_year():
    """Nombre de films par année"""
    try:
        query = """
        SELECT SUBSTRING(release_date, 1, 4) AS year, COUNT(*) AS count
        FROM films
        WHERE release_date IS NOT NULL AND release_date != ''
        GROUP BY year
        ORDER BY year;
        """
        results = con.execute(query).fetchall()
        return [{"year": r[0], "count": r[1]} for r in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
