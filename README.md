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
├── backend/            # API REST en FastAPI
├── frontend/           # Interface utilisateur avec Streamlit
├── ml/                 # Scripts de modélisation (SVD)
├── scripts/            # Scripts de préparation des données (fetch, clean, load DuckDB)
├── data/
│   └── raw/
│       └── ratings.csv  # ⚠️ Fichier obligatoire : données de ratings
├── docker-compose.yml  # Orchestration des services
├── main.py             # Script principal pour exécuter l'ensemble du pipeline
└── start.sh            # Script pour démarrer manuellement les services
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











