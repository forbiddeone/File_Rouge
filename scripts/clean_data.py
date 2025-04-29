import pandas as pd
import os

# --- Paths ---
RAW_FILMS = "data/raw/tmdb_movies.csv"
RAW_RATINGS = "data/raw/ratings.csv"
PROCESSED_FILMS = "data/processed/films_clean.csv"
PROCESSED_RATINGS = "data/processed/ratings_clean.csv"

def main():
    # --- Create processed directory if not exists ---
    os.makedirs("data/processed", exist_ok=True)

    # ============================
    # Nettoyage du fichier films
    # ============================
    print("🔵 Nettoyage du fichier films...")

    films = pd.read_csv(RAW_FILMS)

    # Remove duplicates
    films.drop_duplicates(subset="id", inplace=True)

    # Drop rows with missing important fields
    films.dropna(subset=["id", "title", "description", "release_date"], inplace=True)

    # Convert types
    films["id"] = films["id"].astype(int)
    films["vote_average"] = pd.to_numeric(films["vote_average"], errors="coerce")
    films["vote_count"] = pd.to_numeric(films["vote_count"], errors="coerce")

    # Save cleaned films
    films.to_csv(PROCESSED_FILMS, index=False)
    print(f"✅ Films sauvegardés dans : {PROCESSED_FILMS}")

    # ============================
    # Nettoyage du fichier ratings
    # ============================
    print("🟠 Nettoyage du fichier ratings...")

    # --- Read in small chunks ---
    chunk_size = 100_000
    chunks = []
    n_target = 500_000  # final number of ratings wanted
    n_collected = 0

    for chunk in pd.read_csv(RAW_RATINGS, chunksize=chunk_size):
        chunks.append(chunk)
        n_collected += len(chunk)
        if n_collected >= n_target:
            break

    ratings = pd.concat(chunks, ignore_index=True)

    # If we collected too much, sample exactly 500k
    ratings = ratings.sample(n=500_000, random_state=42)

    # Rename columns
    ratings.rename(columns={"userId": "user_id", "movieId": "film_id"}, inplace=True)

    # Remove duplicates
    ratings.drop_duplicates(subset=["user_id", "film_id"], inplace=True)

    # Drop missing
    ratings.dropna(subset=["user_id", "film_id", "rating", "timestamp"], inplace=True)

    # Keep only ratings where film_id exists in films
    ratings = ratings[ratings["film_id"].isin(films["id"])]

    # Convert types
    ratings["user_id"] = ratings["user_id"].astype(int)
    ratings["film_id"] = ratings["film_id"].astype(int)
    ratings["rating"] = pd.to_numeric(ratings["rating"], errors="coerce")
    ratings["timestamp"] = ratings["timestamp"].astype(int)

    # Save cleaned ratings
    ratings.to_csv(PROCESSED_RATINGS, index=False)
    print(f"✅ Ratings sauvegardés dans : {PROCESSED_RATINGS}")

# --- Ne rien exécuter si importé ailleurs ---
if __name__ == "__main__":
    main()
