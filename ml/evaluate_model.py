import os
import duckdb
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split, cross_validate
from surprise import accuracy

def main():
    # Connexion
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DB_PATH = os.path.join(ROOT_DIR, "data/duckdb/movies.duckdb")
    con = duckdb.connect(DB_PATH)

    # Charger les données
    ratings_df = con.execute("SELECT user_id, film_id, rating FROM ratings LIMIT 100000").fetchdf()

    # Feature Engineering identique
    user_counts = ratings_df['user_id'].value_counts()
    users_to_keep = user_counts[user_counts >= 5].index
    ratings_df = ratings_df[ratings_df['user_id'].isin(users_to_keep)]

    film_counts = ratings_df['film_id'].value_counts()
    films_to_keep = film_counts[film_counts >= 5].index
    ratings_df = ratings_df[ratings_df['film_id'].isin(films_to_keep)]

    ratings_df["rating_centered"] = ratings_df["rating"] - 3.0

    # Préparer pour Surprise
    reader = Reader(rating_scale=(-2.5, 2.5))  # car ratings centrés
    data = Dataset.load_from_df(ratings_df[["user_id", "film_id", "rating_centered"]], reader)

    # Split 70/30
    print("🔵 Évaluation Train/Test 30%")
    trainset, testset = train_test_split(data, test_size=0.3, random_state=42)
    model = SVD()
    model.fit(trainset)
    predictions = model.test(testset)

    rmse = accuracy.rmse(predictions)
    mae = accuracy.mae(predictions)

    print(f"RMSE (split) : {rmse:.4f}")
    print(f"MAE  (split) : {mae:.4f}")

    # Cross-validation 5 folds
    print("\n🟠 Validation croisée (5 folds)")
    cross_results = cross_validate(SVD(), data, measures=["RMSE", "MAE"], cv=5, verbose=True)

    mean_rmse = cross_results["test_rmse"].mean()
    mean_mae = cross_results["test_mae"].mean()

    print(f"RMSE (CV 5 folds) : {mean_rmse:.4f}")
    print(f"MAE  (CV 5 folds) : {mean_mae:.4f}")

if __name__ == "__main__":
    main()
