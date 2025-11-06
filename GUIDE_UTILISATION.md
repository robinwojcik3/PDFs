# 📘 Guide d'Utilisation - PDF Explorer

## 🎯 Objectif

PDF Explorer est une application web interactive en français qui permet d'indexer, d'explorer et d'enseigner les concepts scientifiques à partir de documents PDF.

## 🚀 Installation et Démarrage

### Option 1 : Démarrage Manuel (Recommandé pour le développement)

#### Prérequis
- Python 3.9 ou supérieur
- Node.js 16 ou supérieur
- pip et npm installés

#### Étape 1 : Démarrer le Backend

```bash
# Se placer dans le dossier backend
cd backend

# Créer un environnement virtuel Python (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Démarrer le serveur FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Le backend sera accessible sur : **http://localhost:8000**
Documentation API : **http://localhost:8000/docs**

#### Étape 2 : Démarrer le Frontend

Ouvrir un nouveau terminal :

```bash
# Se placer dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm run dev
```

Le frontend sera accessible sur : **http://localhost:5173**

### Option 2 : Avec Docker Compose

```bash
# À la racine du projet
docker-compose up --build
```

- Frontend : http://localhost:5173
- Backend : http://localhost:8000

## 📚 Utilisation de l'Application

### 1. Ajouter des PDFs

1. Placez vos fichiers PDF dans le dossier `data/pdfs/`
2. Les PDFs peuvent être des articles scientifiques, des rapports, des thèses, etc.

### 2. Indexer les Documents

1. Ouvrez l'application dans votre navigateur : http://localhost:5173
2. Sur la page d'accueil, cliquez sur **"Indexer les documents"**
3. Attendez la fin de l'indexation (un message confirmera le succès)
4. Les documents sont maintenant prêts à être explorés !

### 3. Explorer les Documents

#### Page Documents (`/documents`)

- **Liste complète** de tous les documents indexés
- **Métadonnées** affichées : titre, auteurs, année, nombre de pages
- **Statistiques** : nombre de figures et tableaux
- Cliquez sur un document pour le visualiser en détail

#### Visualisation d'un Document (`/documents/:id`)

**Onglet Sections :**
- Affiche toutes les sections détectées dans le document
- Navigation facile entre les différentes parties
- Contenu complet de chaque section

**Onglet Figures :**
- Galerie de toutes les figures extraites
- Légendes et numéros de page
- Vue miniature avec zoom possible

**Onglet Tableaux :**
- Affichage interactif des tableaux
- Données structurées et lisibles
- Export possible (fonctionnalité future)

**Onglet Annotations :**
- Créer des notes personnelles
- Surligner des passages importants
- Ajouter des commentaires
- Exporter toutes les annotations au format JSON

### 4. Recherche Full-Text (`/search`)

1. Entrez votre requête dans la barre de recherche
2. La recherche s'effectue dans :
   - Les titres
   - Le texte complet
   - Les sections
   - Les abstracts
   - Les mots-clés

3. Les résultats affichent :
   - Le document source
   - Un extrait pertinent (snippet)
   - Un score de pertinence
   - Le numéro de page

### 5. Modules Pédagogiques Interactifs (`/interactive/:id`)

#### Concepts Clés
- **Extraction automatique** des termes les plus importants
- **Visualisation** de la fréquence et de l'importance
- **Mots-clés** du document
- Idéal pour réviser rapidement un document

#### Quiz Pédagogique
- **Questions automatiques** générées à partir du contenu
- Types de questions : choix multiples, vrai/faux
- **Score en temps réel** après soumission
- **Explications** pour chaque réponse
- Parfait pour l'auto-évaluation et l'apprentissage

#### Fiche de Synthèse
- **Vue d'ensemble** complète du document
- **Statistiques** : pages, sections, figures, tableaux
- **Informations** sur les auteurs et l'année
- **Aperçu des sections principales**
- Résumé ou abstract si disponible

#### Statistiques et Visualisations
- **Nombre total de mots** dans le document
- **Moyenne de mots par page**
- **Éléments visuels** (figures + tableaux)
- **Graphique** de distribution des mots par section
- Analyse quantitative du contenu

## 🎨 Fonctionnalités des Annotations

### Créer une Annotation

1. Ouvrez un document
2. Allez dans l'onglet **"Annotations"**
3. Cliquez sur **"Nouvelle annotation"**
4. Choisissez le type :
   - **Note** : Note personnelle (jaune)
   - **Surlignage** : Passage important (doré)
   - **Commentaire** : Remarque détaillée (bleu)
5. Indiquez le numéro de page
6. Rédigez votre annotation
7. Cliquez sur **"Enregistrer"**

### Gérer les Annotations

- **Modifier** : Cliquez sur l'icône crayon
- **Supprimer** : Cliquez sur l'icône corbeille
- **Exporter** : Bouton "Exporter" pour télécharger toutes les annotations en JSON

## 🔍 Conseils d'Utilisation

### Pour la Recherche

- Utilisez des **mots-clés spécifiques** plutôt que des phrases complètes
- Les résultats sont triés par **pertinence**
- La recherche est **insensible à la casse** (majuscules/minuscules)

### Pour les Modules Interactifs

- **Concepts Clés** : Identifiez rapidement les thèmes principaux
- **Quiz** : Testez votre compréhension après lecture
- **Synthèse** : Obtenez une vue d'ensemble avant la lecture détaillée
- **Statistiques** : Comparez la densité d'information entre sections

### Bonnes Pratiques

1. **Indexez régulièrement** les nouveaux PDFs ajoutés
2. **Annotez en lisant** pour une meilleure mémorisation
3. **Utilisez la recherche** pour retrouver rapidement des informations
4. **Explorez les modules interactifs** pour approfondir votre compréhension
5. **Exportez vos annotations** pour les sauvegarder

## 🛠️ Résolution de Problèmes

### Le backend ne démarre pas

```bash
# Vérifiez que toutes les dépendances sont installées
cd backend
pip install -r requirements.txt

# Vérifiez que le port 8000 n'est pas utilisé
lsof -i :8000  # Sur Linux/Mac
netstat -ano | findstr :8000  # Sur Windows
```

### Le frontend ne démarre pas

```bash
# Nettoyez le cache et réinstallez
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Aucun PDF n'est détecté

1. Vérifiez que les PDFs sont bien dans `data/pdfs/`
2. Vérifiez les permissions de lecture du dossier
3. Relancez l'indexation depuis l'interface

### L'indexation échoue

- Vérifiez que les PDFs ne sont pas corrompus
- Assurez-vous que `poppler-utils` est installé (pour pdf2image)
- Consultez les logs du backend pour plus de détails

## 📊 Structure des Données

```
data/
├── pdfs/           # Vos fichiers PDF originaux
├── extracted/      # Figures et images extraites
├── index/          # Index de recherche Whoosh
└── annotations/    # Annotations sauvegardées (JSON)
```

## 🎓 Cas d'Usage Pédagogiques

### Pour les Étudiants
- Annoter des articles pour les révisions
- Créer des fiches de synthèse automatiques
- S'auto-évaluer avec les quiz
- Rechercher rapidement des concepts

### Pour les Enseignants
- Préparer des supports de cours
- Identifier les concepts clés à enseigner
- Créer des quiz pour les étudiants
- Analyser la structure des documents scientifiques

### Pour les Chercheurs
- Indexer une bibliothèque d'articles
- Rechercher dans de nombreux documents
- Annoter et organiser les lectures
- Extraire les données et figures importantes

## 🔄 Mise à Jour

Pour mettre à jour l'application :

```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update
```

## 📞 Support

En cas de problème :
1. Consultez la documentation : `README.md`
2. Vérifiez les logs du backend et frontend
3. Consultez la documentation API : http://localhost:8000/docs

---

**Bonne exploration de vos PDFs scientifiques ! 🚀📚**
