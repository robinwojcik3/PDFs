FROM node:18-alpine

WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste de l'application
COPY . .

# Exposer le port
EXPOSE 5173

# Commande de démarrage
CMD ["npm", "run", "dev", "--", "--host"]
