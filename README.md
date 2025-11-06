# 📚 PDF Explorer v2.0 - Plateforme d'Analyse Scientifique Avancée

Une application web interactive en français pour explorer, analyser et enseigner les concepts scientifiques à partir d'articles de recherche PDF. **Conçue pour chercheurs et experts**.

## 🎯 Vue d'ensemble

PDF Explorer est une plateforme complète d'analyse scientifique qui combine extraction automatique de contenu, analyse méthodologique, visualisation de données et outils pédagogiques interactifs. L'application permet aux chercheurs d'explorer en profondeur la littérature scientifique avec des fonctionnalités avancées d'analyse et d'organisation.

## ✨ Fonctionnalités v2.0

### 🔬 Analyse Scientifique Avancée

#### 1. **Extraction de Bibliographie**
- Détection automatique des citations dans le texte
- Extraction complète de la section bibliographie
- Export BibTeX, RIS, JSON pour gestionnaires de références
- Statistiques de citations (sources les plus citées, types de citations)
- Formatage selon différents styles (APA, IEEE, Chicago)

#### 2. **Détection d'Équations Mathématiques**
- Identification des formules et équations
- Support LaTeX (inline et display)
- Extraction des variables et opérateurs
- Conversion automatique en LaTeX
- Statistiques sur les équations (types, fréquence, complexité)

#### 3. **Analyse de Méthodologie Scientifique**
- Détection automatique du type d'approche (quantitative, qualitative, mixte)
- Identification des méthodes statistiques utilisées
- Analyse du design expérimental (randomisé, contrôlé, en aveugle)
- Extraction des protocoles et étapes méthodologiques
- **Score de rigueur méthodologique** (0-100)
- Informations sur l'échantillon et critères d'inclusion/exclusion
- Évaluation de la validité (interne, externe, fiabilité)

#### 4. **Comparaison de Documents**
- Comparaison pairwise ou multiple
- Analyse de similarité de contenu
- Identification des auteurs et mots-clés communs
- Détection de clusters thématiques
- Matrice de similarité visuelle
- Phrases et sections communes

#### 5. **Système de Recommandations Intelligentes**
- Recommandations basées sur la similarité de contenu
- Recommandations par historique de lecture
- Recherche par thématique/mots-clés
- Recommandations par auteurs
- Identification des sujets tendances
- Réseau de collaborations entre auteurs

### 📊 Organisation et Gestion

#### 6. **Système de Tags et Catégories**
- Tags personnalisés avec couleurs
- Catégories scientifiques prédéfinies :
  - Domaine (Informatique, Physique, Biologie, etc.)
  - Type (Article, Revue, Thèse, etc.)
  - Méthodologie (Expérimentale, Théorique, etc.)
  - Statut de lecture
- Auto-suggestion de tags basée sur le contenu
- Recherche par tags (ET/OU logique)
- Statistiques d'utilisation

#### 7. **Collections et Favoris**
- Création de collections thématiques personnalisées
- Système de favoris avec priorités (1-5)
- Notes personnelles par document
- Couleurs et icônes personnalisables
- Export de collections complètes
- Statistiques par collection

#### 8. **Historique de Lecture**
- Suivi automatique du temps de lecture
- Progression de lecture par page
- Documents récemment consultés
- Statistiques de lecture (temps total, documents lus, sessions)
- Graphiques de lecture par période (jour, semaine, mois)
- Reprise automatique à la dernière page lue

### 🎓 Outils Pédagogiques et Interactifs

#### 9. **Modules Pédagogiques**
- Extraction automatique des concepts clés avec fréquence
- Génération de quiz adaptatifs avec explications
- Fiches de synthèse structurées
- Visualisations statistiques (distribution, graphiques)
- Timeline de recherche par année

#### 10. **Applications Interactives Basées sur les Concepts** 🆕
- **10 types d'applications pédagogiques** générées automatiquement à partir du contenu scientifique
- **Visualisations de données interactives** : Explorer les résultats expérimentaux avec zoom, filtres, comparaisons
- **Simulations scientifiques** : Manipuler les paramètres (croissance, distributions, processus dynamiques)
- **Diagrammes de concepts** : Cartes mentales, flux méthodologiques, réseaux de relations
- **Exercices pratiques** : 3 niveaux (beginner/intermediate/advanced) avec feedback immédiat
- **Calculateurs scientifiques** : Taille d'échantillon, puissance, intervalles de confiance, taille d'effet
- **Timelines de recherche** : Contextualisation historique des découvertes
- **Explorateurs de graphiques** : Analyse approfondie des figures (mesures, annotations, extraction de données)
- **Comparateurs** : Tableaux de données côte-à-côte avec calculs automatiques
- Intégration avec l'analyse méthodologique pour adapter la complexité
- **Conçu pour chercheurs experts** avec nuances scientifiques
- Voir [GUIDE_APPLICATIONS_INTERACTIVES.md](GUIDE_APPLICATIONS_INTERACTIVES.md) pour plus de détails

#### 11. **Export Multi-Formats**
- **Markdown** : Format texte structuré avec sections
- **LaTeX** : Document compilable pour publications
- **JSON** : Export structuré complet avec métadonnées
- **HTML** : Fiches de synthèse imprimables
- Export des annotations avec contexte
- Export de bibliographie (BibTeX, RIS)

### 🔍 Recherche et Indexation

#### 12. **Recherche Full-Text Avancée**
- Indexation complète avec Whoosh
- Recherche dans titres, textes, sections, abstracts
- Snippets avec surlignage
- Suggestions de recherche
- Filtres avancés
- Scores de pertinence

#### 13. **Visualisation et Navigation**
- Affichage des figures extraites
- Tableaux interactifs
- Navigation par sections
- Annotations visuelles
- Aperçu multi-documents

## 🏗️ Architecture Technique

### Backend (Python FastAPI)

```
backend/app/
├── api/
│   ├── documents.py          # Gestion des documents
│   ├── search.py             # Recherche full-text
│   ├── annotations.py        # Annotations
│   ├── interactive.py        # Modules pédagogiques
│   ├── advanced.py           # 🆕 Analyse avancée
│   ├── organization.py       # 🆕 Tags, collections, historique
│   └── learning.py           # 🆕 Applications interactives
├── services/
│   ├── pdf_processor.py           # Extraction PDF
│   ├── search_indexer.py          # Indexation Whoosh
│   ├── annotation_manager.py      # Gestion annotations
│   ├── bibliography_extractor.py  # 🆕 Extraction biblio
│   ├── equation_detector.py       # 🆕 Détection équations
│   ├── methodology_analyzer.py    # 🆕 Analyse méthodologie
│   ├── document_comparator.py     # 🆕 Comparaison
│   ├── recommender.py             # 🆕 Recommandations
│   ├── exporter.py                # 🆕 Export multi-formats
│   ├── tags_manager.py            # 🆕 Gestion tags
│   ├── collections_manager.py     # 🆕 Collections/favoris
│   ├── reading_history.py         # 🆕 Historique lecture
│   └── interactive_generator.py   # 🆕 Générateur d'applications interactives
└── models/
    ├── document.py
    └── annotation.py
```

### Frontend (React + Vite)

```
frontend/src/
├── pages/
│   ├── Home.jsx              # Page d'accueil
│   ├── DocumentList.jsx      # Liste documents
│   ├── DocumentViewer.jsx    # Visualisation document
│   ├── Search.jsx            # Recherche
│   ├── Interactive.jsx       # Modules interactifs
│   └── Advanced.jsx          # 🆕 Analyse avancée
├── components/
│   ├── Layout.jsx
│   └── AnnotationPanel.jsx
└── services/
    └── api.js                # Service API complet
```

### Stockage de Données

```
data/
├── pdfs/           # PDFs originaux
├── extracted/      # Figures et images extraites
├── index/          # Index de recherche Whoosh
├── annotations/    # Annotations (JSON)
├── tags/           # 🆕 Tags et catégories
├── collections/    # 🆕 Collections et favoris
└── history/        # 🆕 Historique de lecture
```

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.9+
- Node.js 16+
- pip et npm

### Méthode 1 : Script Python (Recommandé) ⭐

**Le plus robuste avec fallbacks automatiques et gestion d'erreurs complète**

```bash
python3 start.py
```

**Fonctionnalités :**
- ✅ Détection automatique des ports disponibles (fallback si occupés)
- ✅ Vérification des prérequis (Python, Node.js, npm)
- ✅ Configuration automatique (venv, dépendances)
- ✅ Gestion d'erreurs robuste avec messages clairs
- ✅ Multi-plateforme (Linux, macOS, Windows)
- ✅ Arrêt propre avec Ctrl+C

**Voir [DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md) pour le guide complet**

### Méthode 2 : Scripts Shell

**Linux/Mac :**
```bash
./start.sh
```

**Windows :**
```bash
start.bat
```

### Méthode 3 : Démarrage manuel

**Backend :**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend :**
```bash
cd frontend
npm install
npm run dev
```

### Méthode 4 : Docker Compose
```bash
docker-compose up --build
```

## 🆘 Problèmes de Démarrage ?

Si vous rencontrez des difficultés, consultez :
- **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)** - Guide détaillé avec résolution de problèmes
- Section "Résolution de Problèmes" ci-dessous
- Essayez `python3 start.py` qui gère automatiquement la plupart des problèmes

## 📖 Utilisation

### Démarrage Rapide

1. **Lancer l'application** : http://localhost:5173
2. **Ajouter des PDFs** : Placer vos PDFs dans `data/pdfs/`
3. **Indexer** : Cliquer sur "Indexer les documents"
4. **Explorer** : Naviguer dans les documents indexés

### Fonctionnalités Avancées

#### Analyse de Méthodologie
```
1. Ouvrir un document
2. Aller dans "Modules interactifs" → Puis "Analyse Avancée"
3. Consulter l'onglet "Méthodologie"
4. Voir le score de rigueur et les détails méthodologiques
```

#### Comparaison de Documents
```
1. Sélectionner plusieurs documents
2. API: POST /api/advanced/compare avec IDs
3. Visualiser la matrice de similarité
4. Identifier les clusters thématiques
```

#### Extraction de Bibliographie
```
1. Ouvrir un document
2. Aller dans "Analyse Avancée" → "Bibliographie"
3. Consulter les citations et références
4. Exporter en BibTeX ou RIS
```

#### Système de Tags
```
1. Ouvrir un document
2. Ajouter des tags personnalisés
3. Utiliser les suggestions automatiques
4. Rechercher par tags
```

#### Collections
```
1. Créer une collection thématique
2. Ajouter des documents à la collection
3. Organiser par thème de recherche
4. Exporter la collection
```

## 🔬 Cas d'Usage pour Chercheurs

### 1. Revue de Littérature
- Indexer tous les articles d'un domaine
- Utiliser les tags pour catégoriser
- Comparer les méthodologies
- Identifier les tendances avec les recommandations

### 2. Analyse Méthodologique
- Évaluer la rigueur scientifique (score)
- Comparer les approches expérimentales
- Extraire les protocoles
- Identifier les méthodes statistiques

### 3. Gestion de Bibliographie
- Extraire toutes les références
- Exporter en BibTeX pour LaTeX
- Analyser le réseau de citations
- Identifier les sources clés

### 4. Préparation de Publications
- Comparer avec la littérature existante
- Extraire les équations et formules
- Exporter en format LaTeX
- Identifier les gaps méthodologiques

### 5. Enseignement et Pédagogie
- Créer des quiz à partir du contenu
- Générer des fiches de synthèse
- Visualiser les concepts clés
- Annoter pour les étudiants
- **Générer des applications interactives** pour illustrer les concepts complexes
- Créer des simulations pour explorer les paramètres méthodologiques
- Utiliser des calculateurs pour vérifier les analyses statistiques
- Voir [GUIDE_APPLICATIONS_INTERACTIVES.md](GUIDE_APPLICATIONS_INTERACTIVES.md)

## 📊 API Documentation

L'API complète est documentée avec Swagger UI :
**http://localhost:8000/docs**

### Endpoints Principaux

#### Analyse Avancée (`/api/advanced`)
- `GET /{document_id}/bibliography` - Extraction bibliographie
- `GET /{document_id}/equations` - Détection équations
- `GET /{document_id}/methodology` - Analyse méthodologie
- `POST /compare` - Comparaison de documents
- `GET /{document_id}/recommendations` - Recommandations
- `GET /recommendations/trending-topics` - Sujets tendances
- `GET /{document_id}/export` - Export multi-formats

#### Organisation (`/api/organization`)
- `POST /tags/{document_id}` - Ajouter tag
- `GET /tags/search` - Rechercher par tags
- `POST /collections` - Créer collection
- `POST /favorites/{document_id}` - Ajouter aux favoris
- `POST /history/{document_id}` - Enregistrer lecture
- `GET /history/statistics` - Statistiques de lecture

#### Applications Interactives (`/api/learning`) 🆕
- `GET /{document_id}/interactions` - Toutes les applications pour un document
- `GET /{document_id}/interactions/visualizations` - Visualisations de données
- `GET /{document_id}/interactions/simulations` - Simulations scientifiques
- `GET /{document_id}/interactions/diagrams` - Diagrammes de concepts
- `GET /{document_id}/interactions/exercises` - Exercices pratiques
- `GET /{document_id}/interactions/calculators` - Calculateurs scientifiques
- `GET /{document_id}/interactions/timeline` - Timeline de recherche
- `GET /{document_id}/interactions/graph-explorers` - Explorateurs de graphiques
- `GET /{document_id}/interactions/comparisons` - Comparateurs de données
- `GET /types` - Types d'interactions disponibles
- `POST /{document_id}/interactions/custom` - Créer interaction personnalisée

## 🛠️ Technologies

### Backend
- **FastAPI** - Framework web moderne
- **Python 3.9+** - Langage principal
- **PyPDF2 & pdfplumber** - Extraction PDF
- **Whoosh** - Indexation full-text
- **Pillow** - Traitement d'images

### Frontend
- **React 18** - Framework UI
- **Vite** - Build tool rapide
- **TailwindCSS** - Styling
- **Recharts** - Visualisations
- **Lucide React** - Icônes

## 📈 Métriques et Performances

- **Extraction PDF** : ~2-5 secondes par document
- **Indexation** : ~100 documents/minute
- **Recherche** : < 100ms pour 1000 documents
- **Score de rigueur** : Basé sur 6 critères méthodologiques
- **Similarité** : Algorithme Jaccard + SequenceMatcher

## 🔐 Confidentialité

Toutes les données sont stockées localement :
- Aucune connexion externe requise
- PDFs restent sur votre machine
- Annotations privées
- Historique local uniquement

## 📝 Contribuer

Les contributions sont bienvenues ! Domaines prioritaires :
- Amélioration de l'extraction d'équations
- Support OCR pour PDFs scannés
- Intégration gestionnaires de références (Zotero, Mendeley)
- Export PowerPoint pour présentations
- Visualisation de réseaux de citations

## 🐛 Résolution de Problèmes

### L'indexation échoue
```bash
# Vérifier les dépendances
pip install -r requirements.txt --upgrade

# Vérifier les permissions
chmod 755 data/pdfs/
```

### Les équations ne sont pas détectées
- Vérifier que le PDF contient du texte (pas une image scannée)
- Les équations doivent être en format texte ou LaTeX

### Score de rigueur bas
- Normal si la méthodologie n'est pas claire dans le texte
- Le score évalue : section méthodologie, design, méthodes statistiques, échantillon, validité

## 📚 Documentation

- **[Démarrage Rapide](DEMARRAGE_RAPIDE.md)** ⭐ - Guide de démarrage avec résolution de problèmes
- [Guide d'utilisation complet](GUIDE_UTILISATION.md)
- [Liste des fonctionnalités v2.0](NOUVELLES_FONCTIONNALITES.md)
- **[Guide des Applications Interactives](GUIDE_APPLICATIONS_INTERACTIVES.md)** 🆕
- [Système d'Applications Interactives](SYSTEME_APPLICATIONS_INTERACTIVES.md) - Résumé technique
- [API Documentation](http://localhost:8000/docs)

## 🎓 Citations

Si vous utilisez PDF Explorer dans vos travaux de recherche, veuillez citer :

```bibtex
@software{pdf_explorer_2024,
  title = {PDF Explorer: Plateforme d'Analyse Scientifique Avancée},
  author = {PDF Explorer Contributors},
  year = {2024},
  version = {2.0},
  url = {https://github.com/votre-repo/pdf-explorer}
}
```

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/votre-repo/pdf-explorer/issues)
- **Documentation** : [Wiki](https://github.com/votre-repo/pdf-explorer/wiki)
- **API Docs** : http://localhost:8000/docs

## 🎯 Roadmap v2.1

- [ ] OCR pour PDFs scannés (Tesseract)
- [ ] Extraction de datasets et protocoles
- [ ] Intégration Zotero/Mendeley
- [ ] Analyse de reproductibilité
- [ ] Export PowerPoint
- [ ] Support multilingue (EN, ES, DE)
- [ ] Mode collaboratif
- [ ] API publique avec authentification

## 📄 Licence

MIT License - Voir [LICENSE](LICENSE)

---

**PDF Explorer v2.0** - Développé pour les chercheurs, par des chercheurs 🔬📚
