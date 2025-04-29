#!/bin/bash

# Fonction pour arrêter proprement les processus
cleanup() {
    echo "🛑 Arrêt du backend FastAPI..."
    kill $BACK_PID 2>/dev/null
    exit 1
}

# Vérifications
if [ ! -d "backend/app" ]; then
  echo "❌ Dossier 'backend/app/' introuvable. Place-toi à la racine du projet."
  exit 1
fi

if [ ! -f "frontend/app.py" ]; then
  echo "❌ Fichier 'frontend/app.py' introuvable. Vérifie ton projet."
  exit 1
fi

# Lancer le backend FastAPI
echo "🚀 Lancement du backend FastAPI..."
export PYTHONPATH=./backend
uvicorn backend.app.main:app --reload &
BACK_PID=$!

# Attendre quelques secondes pour s'assurer que le backend démarre
sleep 3

# Lancer le frontend Streamlit
echo "🚀 Lancement du frontend Streamlit..."
streamlit run frontend/app.py || cleanup

# Nettoyer en cas d'arrêt du frontend
cleanup
