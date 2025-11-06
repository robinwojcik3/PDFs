# 🚀 Démarrage Rapide de PDF Explorer

## Méthodes de Démarrage

PDF Explorer offre **3 façons de démarrer** l'application, avec des fallbacks automatiques pour assurer un démarrage réussi dans tous les cas.

## 🎯 Option 1 : Script Python (Recommandé)

**Le plus robuste avec gestion d'erreurs complète et fallbacks automatiques**

```bash
python3 start.py
```

### Fonctionnalités du script Python :

✅ **Détection automatique des ports disponibles**
   - Ports par défaut : Backend (8000), Frontend (5173)
   - Fallbacks automatiques si ports occupés : 8001, 8080, 8888, 9000 (backend) / 5174, 3000, 3001, 4000 (frontend)
   - Trouve un port aléatoire si tous les ports préférés sont occupés

✅ **Vérification des prérequis**
   - Python 3.7+ (3.9+ recommandé)
   - Node.js et npm
   - Affichage des versions détectées

✅ **Configuration automatique**
   - Création de l'environnement virtuel Python si absent
   - Installation automatique des dépendances Python
   - Installation automatique des dépendances Node.js

✅ **Gestion d'erreurs robuste**
   - Continue même si une partie échoue
   - Mode "frontend seul" si backend échoue
   - Mode "backend seul" si frontend échoue
   - Messages d'erreur clairs avec suggestions de résolution

✅ **Arrêt propre**
   - Gestion de Ctrl+C
   - Nettoyage automatique des processus
   - Aucun processus zombie

✅ **Multi-plateforme**
   - Linux, macOS, Windows
   - Gestion automatique des différences (npm vs npm.cmd, chemins, etc.)

## 🐚 Option 2 : Script Bash (Linux/macOS)

**Simple et efficace pour Linux/macOS**

```bash
./start.sh
```

**Ou**

```bash
bash start.sh
```

### Fonctionnalités :

- Démarrage parallèle du backend et frontend
- Configuration automatique de l'environnement virtuel
- Installation des dépendances
- Logs colorés
- Arrêt propre avec Ctrl+C

## 💻 Option 3 : Script Batch (Windows)

```batch
start.bat
```

**Ou double-cliquez sur `start.bat` dans l'explorateur Windows**

### Fonctionnalités :

- Démarrage des deux services
- Configuration de base
- Compatible Windows

## 📋 Prérequis

Avant de démarrer, assurez-vous d'avoir installé :

### Python 3.9+

**Vérifier :**
```bash
python3 --version
# ou
python --version
```

**Installer :**
- Linux : `sudo apt install python3 python3-venv python3-pip`
- macOS : `brew install python3`
- Windows : https://www.python.org/downloads/

### Node.js 16+ et npm

**Vérifier :**
```bash
node --version
npm --version
```

**Installer :**
- Linux : `sudo apt install nodejs npm`
- macOS : `brew install node`
- Windows : https://nodejs.org/

## 🎨 Exemples de Démarrage

### Démarrage Normal

```bash
$ python3 start.py

============================================================
🚀 Démarrage de PDF Explorer
============================================================

ℹ Vérification des prérequis...
✓ Python 3.11.5 détecté
✓ Port 8000 disponible pour le backend
✓ Port 5173 disponible pour le frontend

ℹ Configuration du backend...
✓ Environnement virtuel créé
✓ Dépendances Python installées

ℹ Démarrage du backend FastAPI sur le port 8000...
✓ Backend démarré sur http://localhost:8000
ℹ Documentation API : http://localhost:8000/docs

✓ Node.js v18.17.1 détecté
✓ npm 9.8.1 détecté

ℹ Configuration du frontend...
✓ Dépendances Node.js déjà installées

ℹ Démarrage du frontend React sur le port 5173...
✓ Frontend démarré sur http://localhost:5173

============================================================
✓ Application démarrée !
============================================================

📖 Application web : http://localhost:5173
📚 Documentation API : http://localhost:8000/docs

ℹ Appuyez sur Ctrl+C pour arrêter les services...
```

### Démarrage avec Ports Occupés (Fallback Automatique)

```bash
$ python3 start.py

============================================================
🚀 Démarrage de PDF Explorer
============================================================

ℹ Vérification des prérequis...
✓ Python 3.11.5 détecté
⚠ Port 8000 occupé, utilisation du port 8001
⚠ Port 5173 occupé, utilisation du port 5174

ℹ Démarrage du backend FastAPI sur le port 8001...
✓ Backend démarré sur http://localhost:8001

ℹ Démarrage du frontend React sur le port 5174...
✓ Frontend démarré sur http://localhost:5174

============================================================
✓ Application démarrée !
============================================================

📖 Application web : http://localhost:5174
📚 Documentation API : http://localhost:8001/docs
```

### Mode Dégradé (Backend Seul)

Si Node.js n'est pas installé, le script démarre uniquement le backend :

```bash
$ python3 start.py

...
✗ Node.js n'est pas installé ou n'est pas dans le PATH
ℹ Téléchargez Node.js depuis : https://nodejs.org/

✓ Backend démarré sur http://localhost:8000
ℹ Le backend REST API est accessible sur http://localhost:8000/docs
```

## 🔧 Résolution de Problèmes

### Problème : Port déjà utilisé

**Solution automatique :** Le script `start.py` détecte automatiquement et utilise un port alternatif.

**Solution manuelle :**
```bash
# Trouver le processus utilisant le port
# Linux/macOS :
lsof -i :8000
kill -9 <PID>

# Windows :
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problème : Dépendances Python manquantes

**Solution automatique :** Le script installe automatiquement les dépendances.

**Solution manuelle :**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Problème : Dépendances Node.js manquantes

**Solution automatique :** Le script installe automatiquement les dépendances.

**Solution manuelle :**
```bash
cd frontend
npm install
```

### Problème : Le backend ne démarre pas

**Causes possibles :**
1. Python < 3.7
2. Dépendances manquantes
3. Port déjà utilisé

**Solution :**
```bash
# Vérifier la version Python
python3 --version

# Réinstaller les dépendances
cd backend
pip install -r requirements.txt --upgrade

# Démarrer manuellement avec un port spécifique
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 9000
```

### Problème : Le frontend ne démarre pas

**Causes possibles :**
1. Node.js non installé
2. Dépendances manquantes
3. Port déjà utilisé

**Solution :**
```bash
# Vérifier Node.js
node --version
npm --version

# Réinstaller les dépendances
cd frontend
rm -rf node_modules package-lock.json
npm install

# Démarrer manuellement avec un port spécifique
npm run dev -- --port 4000
```

### Problème : Permission denied sur start.py

**Solution :**
```bash
chmod +x start.py
```

### Problème : ModuleNotFoundError

**Solution :**
```bash
# S'assurer que le venv est activé et réinstaller
cd backend
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

## 🚀 Démarrage Manuel (Sans Script)

Si les scripts ne fonctionnent pas, vous pouvez démarrer manuellement :

### Terminal 1 : Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 : Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📱 Accès à l'Application

Une fois démarrée, accédez à :

- **Application web** : http://localhost:5173 (ou le port indiqué)
- **Documentation API** : http://localhost:8000/docs (ou le port indiqué)
- **API REST** : http://localhost:8000/api

## 🎯 Premiers Pas

1. **Ajoutez des PDFs** : Placez vos PDFs scientifiques dans `data/pdfs/`
2. **Indexez** : Via l'interface web, cliquez sur "Indexer les documents"
3. **Explorez** : Naviguez dans vos documents
4. **Analysez** : Utilisez les fonctionnalités avancées (méthodologie, bibliographie, etc.)
5. **Applications interactives** : Accédez aux applications pédagogiques pour chaque document

## 📚 Documentation Complète

- [README.md](README.md) - Vue d'ensemble du projet
- [GUIDE_APPLICATIONS_INTERACTIVES.md](GUIDE_APPLICATIONS_INTERACTIVES.md) - Guide complet des applications interactives
- [SYSTEME_APPLICATIONS_INTERACTIVES.md](SYSTEME_APPLICATIONS_INTERACTIVES.md) - Résumé technique
- [NOUVELLES_FONCTIONNALITES.md](NOUVELLES_FONCTIONNALITES.md) - Liste des fonctionnalités v2.0

## 💡 Conseils

### Performance

- Le premier démarrage est plus long (installation des dépendances)
- Les démarrages suivants sont plus rapides
- Le mode `--reload` du backend recharge automatiquement lors des modifications

### Développement

- Les modifications du frontend sont appliquées instantanément (hot reload)
- Les modifications du backend redémarrent automatiquement le serveur
- Consultez les logs dans les terminaux pour déboguer

### Production

Pour un déploiement en production, consultez le README principal pour les instructions de build et déploiement.

## 🆘 Support

Si vous rencontrez des problèmes non résolus :

1. Vérifiez les logs d'erreur dans le terminal
2. Consultez la section "Résolution de Problèmes" dans README.md
3. Vérifiez que tous les prérequis sont installés
4. Essayez le démarrage manuel étape par étape

## 🎉 C'est Parti !

```bash
python3 start.py
```

Bonne exploration de vos PDFs scientifiques ! 📚🔬
