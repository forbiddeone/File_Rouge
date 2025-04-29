import duckdb
import shutil
import os

# Crée une copie temporaire de la base pour éviter les conflits de lock
src_path = "data/duckdb/movies.duckdb"
temp_path = "temp_movies.duckdb"

# Supprime si elle existe déjà
if os.path.exists(temp_path):
    os.remove(temp_path)

# Copie de la base
shutil.copy(src_path, temp_path)

# Connexion à la copie
con = duckdb.connect(temp_path)

# Film à tester
film_id = 385687
result = con.execute("SELECT * FROM films WHERE id = ?", (film_id,)).fetchall()

if result:
    print("🎬 Film trouvé :\n", result)
else:
    print("❌ Aucun film trouvé avec cet ID.")

con.close()


