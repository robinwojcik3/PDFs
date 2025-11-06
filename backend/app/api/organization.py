"""
API endpoints pour l'organisation des documents (tags, collections, favoris, historique).
"""
from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional
from pydantic import BaseModel

from app.services.tags_manager import TagsManager
from app.services.collections_manager import CollectionsManager
from app.services.reading_history import ReadingHistory

router = APIRouter()

# Initialiser les services
tags_manager = TagsManager()
collections_manager = CollectionsManager()
reading_history = ReadingHistory()

# === MODELS ===

class TagCreate(BaseModel):
    tag: str
    color: Optional[str] = None

class CategorySet(BaseModel):
    category_type: str
    category_value: str

class CollectionCreate(BaseModel):
    name: str
    description: str = ""
    color: str = "#3b82f6"
    icon: str = "folder"

class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None

class FavoriteCreate(BaseModel):
    priority: int = 3  # 1-5
    notes: str = ""

class ReadingRecord(BaseModel):
    page: Optional[int] = None
    duration_seconds: Optional[int] = None

# === TAGS ===

@router.post("/tags/{document_id}")
async def add_tag(document_id: str, data: TagCreate):
    """Ajoute un tag à un document."""
    result = tags_manager.add_tag(document_id, data.tag, data.color)

    if result:
        return {"message": "Tag ajouté", "tag": result}
    else:
        return {"message": "Tag déjà existant"}

@router.delete("/tags/{document_id}/{tag}")
async def remove_tag(document_id: str, tag: str):
    """Retire un tag d'un document."""
    success = tags_manager.remove_tag(document_id, tag)

    if success:
        return {"message": "Tag supprimé"}
    else:
        raise HTTPException(status_code=404, detail="Tag non trouvé")

@router.get("/tags/{document_id}")
async def get_document_tags(document_id: str):
    """Récupère tous les tags d'un document."""
    tags = tags_manager.get_tags(document_id)
    return {"document_id": document_id, "tags": tags}

@router.get("/tags")
async def get_all_tags():
    """Récupère tous les tags utilisés avec leur fréquence."""
    tags = tags_manager.get_all_tags()
    return {"tags": tags, "total": len(tags)}

@router.get("/tags/search")
async def search_by_tags(
    tags: List[str] = Query(...),
    match_all: bool = Query(False)
):
    """Recherche des documents par tags."""
    documents = tags_manager.search_by_tags(tags, match_all=match_all)

    return {
        "tags": tags,
        "match_all": match_all,
        "documents": documents,
        "count": len(documents)
    }

@router.get("/tags/suggestions/{document_id}")
async def suggest_tags(document_id: str):
    """Suggère des tags pour un document."""
    from app.api.documents import documents_cache

    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id]
    existing_tags = [t['name'] for t in tags_manager.get_tags(document_id)]
    keywords = document.metadata.keywords

    suggestions = tags_manager.suggest_tags(keywords, existing_tags)

    return {
        "document_id": document_id,
        "suggestions": suggestions
    }

# === CATEGORIES ===

@router.post("/categories/{document_id}")
async def set_category(document_id: str, data: CategorySet):
    """Définit une catégorie pour un document."""
    result = tags_manager.set_category(document_id, data.category_type, data.category_value)

    return {"message": "Catégorie définie", "category": result}

@router.get("/categories/{document_id}")
async def get_categories(document_id: str):
    """Récupère les catégories d'un document."""
    categories = tags_manager.get_categories(document_id)

    return {"document_id": document_id, "categories": categories}

@router.get("/categories/predefined")
async def get_predefined_categories():
    """Récupère les catégories prédéfinies."""
    categories = tags_manager.get_predefined_categories()

    return {"categories": categories}

@router.get("/categories/search/{category_type}/{category_value}")
async def search_by_category(category_type: str, category_value: str):
    """Recherche des documents par catégorie."""
    documents = tags_manager.get_documents_by_category(category_type, category_value)

    return {
        "category_type": category_type,
        "category_value": category_value,
        "documents": documents,
        "count": len(documents)
    }

# === COLLECTIONS ===

@router.post("/collections")
async def create_collection(data: CollectionCreate):
    """Crée une nouvelle collection."""
    collection = collections_manager.create_collection(
        name=data.name,
        description=data.description,
        color=data.color,
        icon=data.icon
    )

    return {"message": "Collection créée", "collection": collection}

@router.get("/collections")
async def get_collections():
    """Récupère toutes les collections."""
    collections = collections_manager.get_collections()

    return {"collections": collections, "count": len(collections)}

@router.get("/collections/{collection_id}")
async def get_collection(collection_id: str):
    """Récupère une collection spécifique."""
    collection = collections_manager.get_collection(collection_id)

    if not collection:
        raise HTTPException(status_code=404, detail="Collection non trouvée")

    return collection

@router.put("/collections/{collection_id}")
async def update_collection(collection_id: str, data: CollectionUpdate):
    """Met à jour une collection."""
    collection = collections_manager.update_collection(
        collection_id=collection_id,
        name=data.name,
        description=data.description,
        color=data.color,
        icon=data.icon
    )

    if not collection:
        raise HTTPException(status_code=404, detail="Collection non trouvée")

    return {"message": "Collection mise à jour", "collection": collection}

@router.delete("/collections/{collection_id}")
async def delete_collection(collection_id: str):
    """Supprime une collection."""
    success = collections_manager.delete_collection(collection_id)

    if not success:
        raise HTTPException(status_code=404, detail="Collection non trouvée")

    return {"message": "Collection supprimée"}

@router.post("/collections/{collection_id}/documents/{document_id}")
async def add_to_collection(collection_id: str, document_id: str):
    """Ajoute un document à une collection."""
    success = collections_manager.add_document_to_collection(collection_id, document_id)

    if not success:
        raise HTTPException(status_code=404, detail="Collection non trouvée")

    return {"message": "Document ajouté à la collection"}

@router.delete("/collections/{collection_id}/documents/{document_id}")
async def remove_from_collection(collection_id: str, document_id: str):
    """Retire un document d'une collection."""
    success = collections_manager.remove_document_from_collection(collection_id, document_id)

    if not success:
        raise HTTPException(status_code=404, detail="Document non trouvé dans la collection")

    return {"message": "Document retiré de la collection"}

@router.get("/collections/document/{document_id}")
async def get_document_collections(document_id: str):
    """Récupère toutes les collections contenant un document."""
    collections = collections_manager.get_document_collections(document_id)

    return {"document_id": document_id, "collections": collections, "count": len(collections)}

# === FAVORIS ===

@router.post("/favorites/{document_id}")
async def add_favorite(document_id: str, data: FavoriteCreate):
    """Ajoute un document aux favoris."""
    favorite = collections_manager.add_favorite(
        document_id=document_id,
        priority=data.priority,
        notes=data.notes
    )

    return {"message": "Ajouté aux favoris", "favorite": favorite}

@router.delete("/favorites/{document_id}")
async def remove_favorite(document_id: str):
    """Retire un document des favoris."""
    success = collections_manager.remove_favorite(document_id)

    if not success:
        raise HTTPException(status_code=404, detail="Favori non trouvé")

    return {"message": "Retiré des favoris"}

@router.put("/favorites/{document_id}")
async def update_favorite(document_id: str, data: FavoriteCreate):
    """Met à jour un favori."""
    favorite = collections_manager.update_favorite(
        document_id=document_id,
        priority=data.priority,
        notes=data.notes
    )

    if not favorite:
        raise HTTPException(status_code=404, detail="Favori non trouvé")

    return {"message": "Favori mis à jour", "favorite": favorite}

@router.get("/favorites")
async def get_favorites(sort_by: str = Query("priority", regex="^(priority|added_at|document_id)$")):
    """Récupère tous les favoris."""
    favorites = collections_manager.get_favorites(sort_by=sort_by)

    return {"favorites": favorites, "count": len(favorites)}

@router.get("/favorites/{document_id}")
async def get_favorite(document_id: str):
    """Récupère un favori spécifique."""
    favorite = collections_manager.get_favorite(document_id)

    if not favorite:
        raise HTTPException(status_code=404, detail="Favori non trouvé")

    return favorite

@router.get("/favorites/{document_id}/check")
async def is_favorite(document_id: str):
    """Vérifie si un document est en favori."""
    is_fav = collections_manager.is_favorite(document_id)

    return {"document_id": document_id, "is_favorite": is_fav}

# === HISTORIQUE ===

@router.post("/history/{document_id}")
async def record_reading(document_id: str, data: ReadingRecord):
    """Enregistre une consultation de document."""
    session = reading_history.record_view(
        document_id=document_id,
        page=data.page,
        duration_seconds=data.duration_seconds
    )

    return {"message": "Consultation enregistrée", "session": session}

@router.put("/history/{document_id}/progress")
async def update_reading_progress(
    document_id: str,
    current_page: int,
    total_pages: int
):
    """Met à jour la progression de lecture."""
    history = reading_history.update_progress(document_id, current_page, total_pages)

    if not history:
        raise HTTPException(status_code=404, detail="Historique non trouvé")

    return {"message": "Progression mise à jour", "history": history}

@router.get("/history/{document_id}")
async def get_reading_history(document_id: str):
    """Récupère l'historique d'un document."""
    history = reading_history.get_history(document_id)

    if not history:
        return {"document_id": document_id, "message": "Aucun historique"}

    return history

@router.get("/history")
async def get_all_history(
    sort_by: str = Query("last_view", regex="^(last_view|total_views|total_time_seconds)$"),
    limit: Optional[int] = Query(None, ge=1, le=100)
):
    """Récupère tout l'historique de lecture."""
    history = reading_history.get_all_history(sort_by=sort_by, limit=limit)

    return {"history": history, "count": len(history)}

@router.get("/history/recent")
async def get_recent_documents(
    days: int = Query(7, ge=1, le=365),
    limit: int = Query(10, ge=1, le=50)
):
    """Récupère les documents récemment consultés."""
    recent = reading_history.get_recent_documents(days=days, limit=limit)

    return {"recent_documents": recent, "count": len(recent), "days": days}

@router.get("/history/statistics")
async def get_reading_statistics():
    """Récupère les statistiques globales de lecture."""
    stats = reading_history.get_reading_statistics()

    return stats

@router.get("/history/statistics/period")
async def get_reading_by_period(period: str = Query("week", regex="^(day|week|month)$")):
    """Récupère les statistiques de lecture par période."""
    stats = reading_history.get_reading_by_period(period=period)

    return stats

@router.delete("/history/{document_id}")
async def clear_document_history(document_id: str):
    """Efface l'historique d'un document."""
    success = reading_history.clear_history(document_id=document_id)

    if not success:
        raise HTTPException(status_code=404, detail="Historique non trouvé")

    return {"message": "Historique effacé"}

@router.delete("/history")
async def clear_all_history():
    """Efface tout l'historique de lecture."""
    reading_history.clear_history()

    return {"message": "Tout l'historique a été effacé"}

# === STATISTIQUES ===

@router.get("/statistics")
async def get_organization_statistics():
    """Récupère les statistiques sur les tags, collections et favoris."""
    tags_stats = tags_manager.get_tag_statistics()
    collections_stats = collections_manager.get_statistics()

    return {
        "tags": tags_stats,
        "collections": collections_stats
    }
