#!/bin/bash

# Script de lancement simplifié pour l'application de clustering SEO

echo "🚀 Lancement de l'application de clustering SEO"
echo "============================================="

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✅ Python détecté: $(python3 --version)"

# Création de l'environnement virtuel si nécessaire
if [ ! -d ".venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de la création de l'environnement virtuel"
        exit 1
    fi
fi

# Activation de l'environnement virtuel
echo "🔄 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Installation des dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

# Vérification et installation du modèle spaCy français
echo "🔍 Vérification du modèle spaCy français..."
python3 -c "import spacy; spacy.load('fr_core_news_sm')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installation du modèle spaCy français..."
    python3 -m spacy download fr_core_news_sm
fi

# Définition des variables d'environnement
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS=4

# Recherche d'un port disponible
PORT=8501
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null; do
    PORT=$((PORT + 1))
done

echo "🌐 Port disponible: $PORT"

# Lancement de l'application
echo "🚀 Lancement de Streamlit..."
echo "📝 L'application sera disponible sur: http://localhost:$PORT"
echo "⏹️  Pour arrêter l'application, utilisez Ctrl+C"
echo ""

streamlit run app.py --server.port $PORT --server.headless true --browser.gatherUsageStats false
