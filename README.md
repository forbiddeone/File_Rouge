# 🎬 Système de Recommandation de Films - Homeflix

Bienvenue sur **Homeflix**, un système de recommandation de films basé sur le filtrage collaboratif.  
Le projet a été développé dans le cadre d’un travail de groupe en Master Data Science.

Ce projet permet de :
- Recommander des films personnalisés à partir des goûts d’un utilisateur.
- Visualiser les tendances de films via un tableau de bord interactif.
- Exposer une API REST pour récupérer des recommandations ou consulter les films.
- Déployer le tout avec **Docker Compose**.

## 🧱 Structure du projet

```
File_Rouge/
├── backend                          # Code du backend (API FastAPI)
│   ├── app                          # Modules FastAPI (routes, modèles, logique)
│   ├── Dockerfile                   # Image Docker pour lancer le backend
│   ├── requirements.txt             # Dépendances Python du backend
│   └── tests                        # Tests unitaires ou d’intégration pour le backend
├── data                             # Données utilisées par l’application
│   ├── duckdb                       # Fichiers DuckDB (base de données locale)
│   ├── processed                    # Données nettoyées et prêtes à l’usage
│   └── raw                          # Données brutes initiales (par ex. téléchargées)
├── docker-compose.yml              # Orchestration Docker (backend + frontend)
├── frontend                         # Code du frontend (interface Streamlit)
│   ├── app.py                       # Point d’entrée principal de l’interface Streamlit
│   ├── Dockerfile                   # Image Docker pour le frontend Streamlit
│   ├── __pycache__                  # Cache Python (à ignorer)
│   ├── requirements.txt             # Dépendances Python du frontend
│   ├── test_frontend.py             # Script de test pour vérifier les fonctions UI
│   └── utils.py                     # Fonctions utilitaires appelant l’API backend
├── HELPME.md                        # Notes d’aide ou pense-bête (probablement perso)
├── main.py                          # Fichier racine – probablement non utilisé
├── ml                               # Code lié au machine learning (recommandations)
│   ├── evaluate_model.py            # Script d’évaluation du modèle
│   ├── __pycache__                  # Cache Python (à ignorer)
│   ├── recommender.py               # Logique de recommandation (ex: filtrage collaboratif)
│   ├── svd_model.pkl                # Modèle entraîné (format pickle)
│   └── train_model.py               # Script d’entraînement du modèle
├── __pycache__                      # Cache Python global (à ignorer)
│   └── tests_runner.cpython-311.pyc # Fichier compilé Python pour les tests
├── README.md                        # Explication du projet, comment le lancer, etc.
├── Red_thread.code-workspace        # Fichier de configuration VSCode (workspace)
├── requirements.txt                 # Dépendances globales (peut-être obsolète ou mixte)
├── scripts                          # Scripts utilitaires de traitement de données
│   ├── clean_data.py                # Nettoyage des données
│   ├── create_duckdb.py             # Initialisation de la base DuckDB
│   ├── fetch_tmdb.py                # Téléchargement des données TMDB (API)
│   ├── __init__.py                  # Rend le dossier importable en tant que module
│   ├── load_ratings_duckdb.py       # Chargement des notes dans DuckDB
│   ├── logger.py                    # Gestion des logs
│   └── __pycache__                  # Cache Python
├── start.sh                         # Script pour démarrer l’application localement
└── tests_runner.py                  # Script de test lancer pour le projet
```


> 🔗 **Télécharger le fichier `ratings.csv` depuis Kaggle** :  
> [https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)

> ⚠️ **Attention** : placez le fichier `ratings.csv` dans le dossier `data/raw/` avant de lancer `main.py` ou le `docker-compose`.

---




## ⚙️ Prérequis & Installation

### 🐍 Environnement local (option manuelle)

1. **Créer un environnement virtuel :**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate     # Windows

## ⚙️ Prérequis & Installation

### 🐍 Environnement local (option manuelle)

1. **Créer un environnement virtuel :**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate     # Windows
```

2. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```
3. **⚠️ S'assurer que le fichier ratings.csv est bien placé dans data/raw/.**

🔗 Télécharger ici : https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

Ensuite, placez-le dans le dossier suivant :

```bash
data/raw/ratings.csv
```
4. **Lancer le script principal (fetch + clean + création de la base DuckDB) :**
```bash
python3 main.py
```

5. **Lancer manuellement l’API et le dashboard frontend :**
```bash
chmod +x start.sh
./start.sh
```
### Utilisation avec Docker (recommandé)
⚠️ Docker & Docker Compose doivent être installés au préalable.
1. **Construire et lancer les services (backend + frontend) :**
```bash
docker-compose up --build -d
```
2. **Consulter les logs des services (optionnel) :**
```bash
docker-compose logs -f

```

3. **Accéder aux interfaces :**

- API REST (FastAPI) : http://localhost:8000
- Dashboard utilisateur (Streamlit) : http://localhost:8501
## 📡 Endpoints de l'API REST (Backend - FastAPI)

Le backend expose plusieurs endpoints pour interagir avec les données des films et générer des recommandations.

### 🔍 1. Détails d’un film

- **Méthode** : `GET`
- **URL** : `/movie/{id}`
- **Description** : Récupère les détails d’un film par son identifiant.
- **Exemple** :
```http
GET http://localhost:8000/movie/107

- Réponse JSON :
```bash
{
  "title": "Snatch",
  "genres": ["Crime", "Comedy"],
  "release_date": "2000-09-01",
  "vote_average": 7.81,
  "vote_count": 9281,
  "description": "Unscrupulous boxing promoters, violent bookmakers, ..."
}
```
###  2. Recommandations pour un utilisateur ###
- Méthode : POST

 - URL : /recommend_movies/{user_id}

- Description : Génère une liste de films recommandés pour l’utilisateur donné, via un modèle SVD.

- Exemple :
  
```bash
POST http://localhost:8000/recommend_movies/107
```

- Réponse JSON :
```bash
  [
  {"title": "Taxi", "rating_predicted": 4.61},
  {"title": "Galaxy Quest", "rating_predicted": 4.47},
  ...
]
```



### 3. Statistiques sur les films
### a. Répartition par genre ###
- Méthode : GET

- URL : /statistics/genres_distribution

### b. Nombre de films par année ###
- Méthode : GET

- URL : /statistics/films_per_year

- Exemple :
- 
```bash
GET http://localhost:8000/statistics/films_per_year
```

## 📊 Fonctionnalités du Dashboard (Frontend - Streamlit)

Le frontend offre une interface interactive simple et efficace pour visualiser les données des films, consulter les tendances, et obtenir des recommandations personnalisées.

---

### 🎬 1. Visualiser les statistiques globales

- **Répartition du nombre de films par année**
- **Distribution des genres de films**
- **Top films notés par genre et par année**

📈 Les données proviennent directement de la base DuckDB ou via l’API FastAPI.

---

### 🔍 2. Obtenir des recommandations personnalisées

- Entrer un **`user_id`**.
- Voir la liste des **films préférés** de cet utilisateur.
- Recevoir des **recommandations de nouveaux films** basées sur son historique.
- Visualiser les **notes prédites** associées aux recommandations.

Exemple de formulaire Streamlit :

> 🎯 "Entrez un ID utilisateur" → **107**  
> ✅ "Films préférés" → *Taxi*, *Fight Club*, etc.  
> 🚀 "Recommandations" → *Galaxy Quest*, *Crouching Tiger, Hidden Dragon*, etc.











