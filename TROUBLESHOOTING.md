# Guide de dépannage - PDF Explorer

## Problème de démarrage résolu

### 1. Erreur Python 3.13 - Whoosh (RÉSOLU)

**Problème :** `KeyError: '__version__'` lors de l'installation des dépendances
**Cause :** Le package `whoosh==2.7.4` n'est pas compatible avec Python 3.13
**Solution :** Remplacement par `Whoosh-reloaded==2.7.4` (fork maintenu compatible avec Python 3.13)

Cette erreur a été corrigée dans le fichier `backend/requirements.txt`.

---

## Configuration requise pour npm (Windows)

### Problème : npm non trouvé dans le PATH

Même si Node.js est installé, npm peut ne pas être accessible dans le PATH système, surtout si Node.js a été installé dans un répertoire avec des espaces.

### Solutions

#### Option 1 : Vérifier l'installation de Node.js et npm

1. Ouvrez PowerShell en tant qu'administrateur
2. Vérifiez l'installation :
   ```powershell
   node --version
   npm --version
   ```

3. Si `node` fonctionne mais pas `npm`, localisez votre installation Node.js :
   ```powershell
   where.exe node
   ```

4. Ajoutez le dossier de Node.js au PATH :
   - Ouvrez "Paramètres système avancés" (recherchez "variables d'environnement")
   - Cliquez sur "Variables d'environnement"
   - Dans "Variables système", trouvez "Path" et cliquez sur "Modifier"
   - Ajoutez le chemin vers votre installation Node.js (par exemple : `C:\Program Files\nodejs\`)
   - Cliquez sur "OK" pour sauvegarder
   - **IMPORTANT :** Redémarrez PowerShell après avoir modifié le PATH

#### Option 2 : Réinstaller Node.js

1. Téléchargez la dernière version LTS depuis https://nodejs.org/
2. **IMPORTANT :** Installez Node.js dans un chemin **sans espaces**, par exemple :
   - `C:\nodejs\` (recommandé)
   - ou utilisez le chemin par défaut `C:\Program Files\nodejs\`
3. Pendant l'installation, cochez la case "Add to PATH"
4. Redémarrez PowerShell après l'installation

#### Option 3 : Utiliser un chemin d'installation sans espaces

Votre installation actuelle semble être dans :
```
C:\Users\utilisateur\Mon Drive\...
```

Les espaces dans "Mon Drive" peuvent causer des problèmes. Considérez :
1. Déplacer le projet vers un chemin sans espaces, par exemple :
   ```
   C:\Projets\PDFs\
   ```
2. Ou utiliser le sous-système Windows pour Linux (WSL2)

---

## Prochaines étapes après la correction

Une fois npm configuré, relancez l'application avec :

```powershell
python start.py
```

L'application devrait maintenant :
1. ✓ Installer correctement les dépendances Python (problème résolu)
2. ✓ Démarrer le backend FastAPI
3. ✓ Installer les dépendances Node.js (après configuration de npm)
4. ✓ Démarrer le frontend React

---

## Tests après configuration

Pour vérifier que tout fonctionne :

```powershell
# Test 1 : Vérifier Python et les dépendances
cd backend
.\venv\Scripts\activate
python -c "import whoosh; print('Whoosh OK')"
python -c "import fastapi; print('FastAPI OK')"
deactivate

# Test 2 : Vérifier npm
npm --version

# Test 3 : Lancer l'application
cd ..
python start.py
```

---

## Support supplémentaire

Si vous rencontrez d'autres problèmes :
1. Vérifiez que Python 3.9+ est installé
2. Vérifiez que Node.js 16+ est installé
3. Assurez-vous d'avoir les droits d'administrateur si nécessaire
4. Vérifiez votre pare-feu (ports 8000 et 5173 doivent être accessibles)
