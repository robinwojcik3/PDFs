# 📚 Application d'Indexation et d'Illustration Interactive de PDFs Scientifiques

Une application web interactive en français pour explorer, indexer et enseigner les concepts scientifiques à partir d'articles PDF.

## 🎯 Fonctionnalités

### 🔍 Exploration et Indexation
- **Scan automatique** des PDFs du dépôt
- **Extraction intelligente** du texte, figures, tableaux et sections
- **Indexation full-text** pour recherche rapide
- **Métadonnées** extraites automatiquement (titre, auteurs, année)

### 📊 Visualisation
- **Affichage des figures** avec zoom et navigation
- **Tableaux interactifs** avec tri et filtrage
- **Structure du document** avec sections cliquables
- **Aperçu PDF** intégré

### 🎓 Outils Pédagogiques
- **Modules interactifs** pour illustrer les concepts clés
- **Quizz et exercices** générés à partir du contenu
- **Visualisations de données** scientifiques
- **Fiches de synthèse** automatiques

### ✏️ Annotation et Collaboration
- **Annotations textuelles** sur les PDFs
- **Surlignage** de passages importants
- **Notes personnelles** sauvegardées
- **Export des annotations**

### 🔎 Recherche Avancée
- **Recherche full-text** dans tous les documents
- **Filtres** par auteur, année, mots-clés
- **Suggestions** de recherche intelligentes
- **Recherche dans les figures et tableaux**

## 🏗️ Architecture

```
pdf-explorer/
├── backend/              # API FastAPI (Python)
│   ├── app/
│   │   ├── api/         # Endpoints REST
│   │   ├── core/        # Configuration
│   │   ├── models/      # Modèles de données
│   │   ├── services/    # Logique métier
│   │   │   ├── pdf_processor.py      # Extraction PDF
│   │   │   ├── search_indexer.py     # Indexation
│   │   │   └── annotation_manager.py # Annotations
│   │   └── main.py
│   └── requirements.txt
├── frontend/            # Interface React
│   ├── src/
│   │   ├── components/  # Composants React
│   │   ├── pages/       # Pages de l'application
│   │   ├── services/    # API calls
│   │   └── App.jsx
│   └── package.json
├── data/
│   ├── pdfs/           # Dossier des PDFs
│   ├── extracted/      # Figures et tableaux extraits
│   └── index/          # Index de recherche
└── docker-compose.yml
```

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.9+
- Node.js 16+
- Docker (optionnel)

### Méthode 1 : Démarrage Manuel

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Méthode 2 : Docker Compose
```bash
docker-compose up
```

## 📖 Utilisation

1. **Démarrer l'application** : Accéder à http://localhost:5173
2. **Ajouter des PDFs** : Placer vos PDFs dans le dossier `data/pdfs/`
3. **Indexer** : Cliquer sur "Indexer les documents" dans l'interface
4. **Explorer** : Naviguer dans les documents, figures et tableaux
5. **Annoter** : Utiliser les outils d'annotation sur les documents
6. **Rechercher** : Utiliser la barre de recherche full-text

## 🛠️ Technologies

- **Backend** : FastAPI, Python, PyPDF2, pdfplumber, Pillow
- **Frontend** : React, Vite, TailwindCSS, Recharts
- **Recherche** : Whoosh (indexation full-text)
- **Base de données** : SQLite (annotations et métadonnées)

## 📝 Licence

MIT
