"""
API endpoints pour la recherche dans les documents.
"""
from fastapi import APIRouter, Query
from typing import List, Optional

from app.models.document import SearchResult
from app.services.search_indexer import SearchIndexer

router = APIRouter()
search_indexer = SearchIndexer()

@router.get("/", response_model=List[SearchResult])
async def search_documents(
    q: str = Query(..., description="Requête de recherche"),
    limit: int = Query(20, ge=1, le=100, description="Nombre maximum de résultats")
):
    """
    Recherche full-text dans tous les documents indexés.

    Args:
        q: Requête de recherche
        limit: Nombre maximum de résultats (1-100)

    Returns:
        Liste de résultats triés par pertinence
    """
    results = search_indexer.search(q, limit=limit)
    return results

@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=2, description="Début de la requête"),
    limit: int = Query(5, ge=1, le=10)
):
    """
    Retourne des suggestions de recherche.

    Args:
        q: Début de la requête (minimum 2 caractères)
        limit: Nombre de suggestions (1-10)
    """
    suggestions = search_indexer.get_suggestions(q, limit=limit)
    return {"suggestions": suggestions}

@router.post("/reindex")
async def reindex_all():
    """
    Réindexe tous les documents.
    Utile après des modifications de l'algorithme d'indexation.
    """
    search_indexer.clear_index()
    return {"message": "Index vidé avec succès. Relancez l'indexation des documents."}
