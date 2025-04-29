import duckdb
import pandas as pd
import os

def main():
    # Chargement des données
    films = pd.read_csv("data/processed/films_clean.csv")
    ratings = pd.read_csv("data/processed/ratings_clean.csv")

    # Création du dossier data/duckdb si nécessaire
    os.makedirs("data/duckdb", exist_ok=True)

    # Connexion à la base
    con = duckdb.connect("data/duckdb/movies.duckdb")

    # Suppression des tables si elles existent
    con.execute("DROP TABLE IF EXISTS ratings;")
    con.execute("DROP TABLE IF EXISTS films;")

    # Création de la table films
    con.execute("""
    CREATE TABLE films (
        id INTEGER PRIMARY KEY,
        title TEXT,
        genres TEXT,
        description TEXT,
        release_date TEXT,
        vote_average DOUBLE,
        vote_count INTEGER
    );
    """)

    # Création de la table ratings
    con.execute("""
    CREATE TABLE ratings (
        user_id INTEGER,
        film_id INTEGER,
        rating DOUBLE,
        timestamp INTEGER,
        PRIMARY KEY(user_id, film_id),
        FOREIGN KEY(film_id) REFERENCES films(id)
    );
    """)

    # Insertion des données
    con.register("films_df", films)
    con.execute("INSERT INTO films SELECT * FROM films_df;")

    con.register("ratings_df", ratings)
    con.execute("INSERT INTO ratings SELECT * FROM ratings_df;")

    # Test simple
    nb_films = con.execute("SELECT COUNT(*) FROM films").fetchone()[0]
    nb_ratings = con.execute("SELECT COUNT(*) FROM ratings").fetchone()[0]

    # Fermeture
    con.close()

    print("Base DuckDB créée avec succès.")
    print(f"{nb_films} films insérés.")
    print(f"{nb_ratings} ratings insérés.")
