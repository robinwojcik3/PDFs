"""
Application principale FastAPI pour l'indexation et l'illustration de PDFs scientifiques.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api import documents, search, annotations, interactive, advanced, organization

app = FastAPI(
    title="PDF Explorer - Indexation Interactive de PDFs Scientifiques",
    description="Application web pour explorer, annoter et enseigner à partir de PDFs scientifiques",
    version="2.0.0"
)

# Configuration CORS pour le développement local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monter les dossiers statiques pour servir les fichiers extraits
os.makedirs("../data/extracted", exist_ok=True)
os.makedirs("../data/pdfs", exist_ok=True)
os.makedirs("../data/tags", exist_ok=True)
os.makedirs("../data/collections", exist_ok=True)
os.makedirs("../data/history", exist_ok=True)

app.mount("/static/extracted", StaticFiles(directory="../data/extracted"), name="extracted")
app.mount("/static/pdfs", StaticFiles(directory="../data/pdfs"), name="pdfs")

# Inclure les routers
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(search.router, prefix="/api/search", tags=["Recherche"])
app.include_router(annotations.router, prefix="/api/annotations", tags=["Annotations"])
app.include_router(interactive.router, prefix="/api/interactive", tags=["Modules Interactifs"])
app.include_router(advanced.router, prefix="/api/advanced", tags=["Analyse Avancée"])
app.include_router(organization.router, prefix="/api/organization", tags=["Organisation"])

@app.get("/")
async def root():
    """Page d'accueil de l'API."""
    return {
        "message": "Bienvenue sur l'API PDF Explorer - Version 2.0",
        "documentation": "/docs",
        "version": "2.0.0",
        "new_features": [
            "Extraction de bibliographie et équations",
            "Analyse de méthodologie scientifique",
            "Comparaison de documents",
            "Système de tags et catégories",
            "Collections et favoris",
            "Historique de lecture",
            "Recommandations intelligentes",
            "Export multi-formats"
        ]
    }

@app.get("/api/health")
async def health_check():
    """Vérification de l'état de l'API."""
    return {"status": "healthy", "message": "L'API fonctionne correctement"}
