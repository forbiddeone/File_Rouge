'''
import duckdb
import pandas as pd
from surprise import Dataset, Reader, SVD
import pickle
import os

def main():
    # 🔗 Connexion à la base DuckDB
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DB_PATH = os.path.join(ROOT_DIR, "data/duckdb/movies.duckdb")
    con = duckdb.connect(DB_PATH)

    # 📦 Charger un sous-échantillon d'évaluations pour entraîner vite
    ratings_df = con.execute("SELECT user_id, film_id, rating FROM ratings LIMIT 50000").fetchdf()

    # 🔎 Préparer les données pour Surprise
    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(ratings_df, reader)
    trainset = data.build_full_trainset()

    # 🤖 Entraîner un modèle SVD
    model = SVD()
    model.fit(trainset)

    # 💾 Sauvegarder le modèle entraîné
    model_path = os.path.join(ROOT_DIR, "ml/svd_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print("✅ Modèle SVD entraîné et sauvegardé.")

if __name__ == "__main__":
    main()
'''
import os
import duckdb
import pandas as pd
from surprise import Dataset, Reader, SVD
import pickle

def main():
    # Connexion à la base
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DB_PATH = os.path.join(ROOT_DIR, "data/duckdb/movies.duckdb")
    con = duckdb.connect(DB_PATH)

    # Charger les données
    ratings_df = con.execute("SELECT user_id, film_id, rating FROM ratings").fetchdf()

    # Feature Engineering
    user_counts = ratings_df["user_id"].value_counts()
    active_users = user_counts[user_counts >= 5].index
    ratings_df = ratings_df[ratings_df["user_id"].isin(active_users)]

    film_counts = ratings_df["film_id"].value_counts()
    popular_films = film_counts[film_counts >= 5].index
    ratings_df = ratings_df[ratings_df["film_id"].isin(popular_films)]

    ratings_df["rating_centered"] = ratings_df["rating"] - 3.0

    ratings_df = ratings_df.sample(n=50000, random_state=42)

    reader = Reader(rating_scale=(-2.5, 2.5))  # ratings centrés
    data = Dataset.load_from_df(ratings_df[["user_id", "film_id", "rating_centered"]], reader)
    trainset = data.build_full_trainset()

    model = SVD()
    model.fit(trainset)

    model_path = os.path.join(ROOT_DIR, "ml/svd_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print("✅ Modèle SVD entraîné avec Feature Engineering et sauvegardé.")

if __name__ == "__main__":
    main()

