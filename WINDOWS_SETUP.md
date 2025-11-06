# PDF Explorer - Configuration Windows

## Problèmes résolus

### 1. Erreur d'installation Python (KeyError: '__version__')

**Problème :** L'installation échouait avec une erreur `KeyError: '__version__'` lors de l'installation de `python-magic`.

**Solution :** Remplacement de `python-magic` par `python-magic-bin` dans `requirements.txt`. Cette version inclut les binaires Windows nécessaires.

### 2. npm non trouvé dans le PATH

**Problème :** Node.js est installé mais npm n'est pas reconnu.

**Solution :** Vous devez ajouter npm au PATH de Windows :

1. Ouvrez les Paramètres système avancés
2. Cliquez sur "Variables d'environnement"
3. Dans la section "Variables système", trouvez la variable "Path"
4. Ajoutez le chemin vers npm (généralement : `C:\Program Files\nodejs\`)
5. Redémarrez PowerShell/Terminal

**Vérification :** Après avoir redémarré le terminal, exécutez :
```powershell
npm --version
```

## Dépendances système requises

Pour un fonctionnement complet de PDF Explorer, vous devez installer :

### 1. Tesseract OCR (pour l'OCR des PDFs)

**Téléchargement :** https://github.com/UB-Mannheim/tesseract/wiki

**Installation :**
1. Téléchargez l'installateur Windows
2. Installez dans `C:\Program Files\Tesseract-OCR\`
3. Ajoutez au PATH : `C:\Program Files\Tesseract-OCR\`

**Vérification :**
```powershell
tesseract --version
```

### 2. Poppler (pour pdf2image)

**Téléchargement :** https://github.com/oschwartz10612/poppler-windows/releases

**Installation :**
1. Téléchargez la dernière version
2. Extrayez dans `C:\Program Files\poppler\`
3. Ajoutez au PATH : `C:\Program Files\poppler\Library\bin\`

**Vérification :**
```powershell
pdfinfo -v
```

## Démarrage de l'application

Après avoir résolu ces problèmes, démarrez l'application avec :

```powershell
python start.py
```

## Si les problèmes persistent

### Nettoyage complet

Si vous rencontrez toujours des problèmes, effectuez un nettoyage complet :

```powershell
# Supprimer l'environnement virtuel
Remove-Item -Recurse -Force backend\venv

# Supprimer les modules Node.js
Remove-Item -Recurse -Force frontend\node_modules

# Relancer le script de démarrage
python start.py
```

### Installation manuelle des dépendances

Si le script automatique échoue, installez manuellement :

**Backend :**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend :**
```powershell
cd frontend
npm install
```

**Démarrage manuel :**

Terminal 1 (Backend) :
```powershell
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 (Frontend) :
```powershell
cd frontend
npm run dev
```

## Support

Si vous rencontrez d'autres problèmes, consultez les logs d'erreur complets et vérifiez que :
- Python 3.9+ est installé
- Node.js 18+ est installé
- Toutes les variables PATH sont correctement configurées
- Vous avez les droits d'administrateur si nécessaire
