import os
import pickle
import pandas as pd

def load_model():
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model_path = os.path.join(ROOT_DIR, "ml/svd_model.pkl")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def get_recommendations_for_user(user_id: int, con, n: int = 5):
    from surprise import Dataset, Reader

    # Charger les données
    ratings_df = con.execute("SELECT user_id, film_id, rating FROM ratings").fetchdf()
    films_df = con.execute("SELECT id, title FROM films").fetchdf()

    # Feature engineering identique
    user_counts = ratings_df["user_id"].value_counts()
    active_users = user_counts[user_counts >= 5].index
    ratings_df = ratings_df[ratings_df["user_id"].isin(active_users)]

    film_counts = ratings_df["film_id"].value_counts()
    popular_films = film_counts[film_counts >= 5].index
    ratings_df = ratings_df[ratings_df["film_id"].isin(popular_films)]

    ratings_df["rating_centered"] = ratings_df["rating"] - 3.0

    # Films non notés par l'utilisateur
    user_rated = ratings_df[ratings_df["user_id"] == user_id]["film_id"].tolist()
    all_unrated = films_df[~films_df["id"].isin(user_rated)]

    # Charger modèle
    model = load_model()

    predictions = []
    for _, row in all_unrated.iterrows():
        pred = model.predict(uid=user_id, iid=row["id"])
        real_rating = pred.est + 3.0  # ➡️ ajouter 3.0 car ratings centrés
        predictions.append({
            "id": row["id"],
            "title": row["title"],
            "rating_predicted": round(real_rating, 2)
        })

    return sorted(predictions, key=lambda x: x["rating_predicted"], reverse=True)[:n]
