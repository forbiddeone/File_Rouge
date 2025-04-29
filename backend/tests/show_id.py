# backend/tests/show_ids.py

import duckdb

con = duckdb.connect("data/duckdb/movies.duckdb")

print("🎬 Films disponibles :")
films = con.execute("SELECT id, title FROM films LIMIT 20").fetchall()
for fid, title in films:
    print(f"ID {fid} → {title}")

print("\n👤 Utilisateurs ayant noté des films :")
users = con.execute("SELECT DISTINCT user_id FROM ratings LIMIT 20").fetchall()
for (uid,) in users:
    print(f"user_id = {uid}")
        
con.close()


