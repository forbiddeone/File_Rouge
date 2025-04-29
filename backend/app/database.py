import duckdb
import os
import shutil

# Mode test activé ?
IS_TEST = os.environ.get("IS_TEST", "false").lower() == "true"

# Chemin réel vers la base principale
original_db_path = "data/duckdb/movies.duckdb"

if IS_TEST:
    test_db_path = "data/duckdb/test_movies.duckdb"
    shutil.copyfile(original_db_path, test_db_path)
    con = duckdb.connect(test_db_path)
else:
    con = duckdb.connect(original_db_path)
