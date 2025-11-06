#!/bin/bash

# Script de démarrage pour PDF Explorer
# Ce script démarre le backend et le frontend en parallèle

echo "🚀 Démarrage de PDF Explorer..."
echo ""

# Couleurs pour les logs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour démarrer le backend
start_backend() {
    echo -e "${BLUE}📦 Démarrage du backend FastAPI...${NC}"
    cd backend

    # Créer l'environnement virtuel s'il n'existe pas
    if [ ! -d "venv" ]; then
        echo "Création de l'environnement virtuel Python..."
        python3 -m venv venv
    fi

    # Activer l'environnement virtuel
    source venv/bin/activate

    # Installer les dépendances
    echo "Installation des dépendances Python..."
    pip install -q -r requirements.txt

    # Démarrer le serveur
    echo -e "${GREEN}✓ Backend démarré sur http://localhost:8000${NC}"
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# Fonction pour démarrer le frontend
start_frontend() {
    echo -e "${BLUE}⚛️  Démarrage du frontend React...${NC}"
    cd frontend

    # Installer les dépendances si nécessaire
    if [ ! -d "node_modules" ]; then
        echo "Installation des dépendances Node.js..."
        npm install
    fi

    # Démarrer le serveur de développement
    echo -e "${GREEN}✓ Frontend démarré sur http://localhost:5173${NC}"
    npm run dev
}

# Démarrer les deux services en parallèle
start_backend &
BACKEND_PID=$!

sleep 5  # Attendre que le backend démarre

start_frontend &
FRONTEND_PID=$!

# Attendre que l'utilisateur arrête les services
echo ""
echo -e "${GREEN}✓ Application démarrée !${NC}"
echo ""
echo "📖 Accédez à l'application : http://localhost:5173"
echo "📚 Documentation API : http://localhost:8000/docs"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter les services..."

# Gérer l'arrêt propre
trap "echo 'Arrêt des services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

wait
