from tests_runner import run_backend_tests, run_frontend_tests
from scripts import clean_data, create_duckdb, fetch_tmdb
from ml import train_model, evaluate_model

def main():
    print("🔵 Nettoyage des données...")
    clean_data.main()

    print("🟣 Création de la BDD DuckDB...")
    create_duckdb.main()

    print("🔵 Récupération des films TMDB...")
    fetch_tmdb.main()

    print("🟠 Entraînement du modèle...")
    train_model.main()

    print("🟢 Évaluation du modèle...")
    evaluate_model.main()

    print("🧪 Lancement des tests...")
    run_backend_tests()
    run_frontend_tests()

if __name__ == "__main__":
    main()
