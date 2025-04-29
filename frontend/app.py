import streamlit as st
import pandas as pd
import plotly.express as px
from utils import (
    get_movie_by_id,
    get_recommendations,
    get_genre_distribution,
    get_films_per_year
)

st.set_page_config(page_title="Système de recommandation de films", layout="centered")
st.title("🎬 Système de Recommandation de Films")

# --- 1. Détail d’un film par ID
with st.expander("📂 Détails d’un film"):
    movie_id = st.number_input("ID du film", min_value=1, step=1, value=550)
    if st.button("Afficher les détails du film"):
        film = get_movie_by_id(movie_id)
        if film and "title" in film:
            st.success(f"🎥 {film['title']}")
            st.write(f"📅 Année : {film.get('year', 'Inconnue')}")
            st.write(f"🎭 Genres : {film.get('genres', 'Non renseignés')}")

            st.subheader("📝 Détails supplémentaires")
            if 'description' in film:
                st.write(f"**Résumé** : {film['description']}")
            if 'release_date' in film:
                st.write(f"**Date de sortie** : {film['release_date']}")
            if 'vote_average' in film:
                st.write(f"**Note moyenne** : {round(film['vote_average'], 2)} ⭐")
            if 'vote_count' in film:
                st.write(f"**Nombre de votes** : {film['vote_count']:,}")

        else:
            st.warning("Film non trouvé ou erreur backend.")

# --- 2. Recommandations personnalisées
with st.expander("🧠 Recommandations personnalisées"):
    user_id = st.number_input("ID de l'utilisateur", min_value=1, step=1)
    if st.button("Obtenir des recommandations"):
        recos = get_recommendations(user_id)
        if recos and isinstance(recos, list) and "error" not in recos[0]:
            for r in recos:
                st.markdown(f"**🎞️ {r['title']}** — ⭐ {round(r['rating_predicted'], 2)}")
        else:
            st.warning("Aucune recommandation trouvée ou erreur backend.")

# --- 3. Statistiques des films
with st.expander("📊 Statistiques des films"):

    st.subheader("📈 Répartition des genres")
    genres = get_genre_distribution()
    if genres:
        df_genres = pd.DataFrame(genres)
        fig = px.bar(df_genres, x="genre", y="count", title="Genres les plus fréquents")
        st.plotly_chart(fig)
    else:
        st.warning("Impossible de charger les genres.")

    st.subheader("📅 Nombre de films par année")
    years = get_films_per_year()
    if years:
        df_years = pd.DataFrame(years)
        fig2 = px.line(df_years, x="year", y="count", title="Films sortis par année")
        st.plotly_chart(fig2)
    else:
        st.warning("Impossible de charger les données par année.")
