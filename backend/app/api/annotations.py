"""
API endpoints pour la gestion des annotations.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models.annotation import Annotation, AnnotationCreate, AnnotationUpdate
from app.services.annotation_manager import AnnotationManager

router = APIRouter()
annotation_manager = AnnotationManager()

@router.post("/", response_model=Annotation)
async def create_annotation(data: AnnotationCreate):
    """Crée une nouvelle annotation sur un document."""
    try:
        annotation = annotation_manager.create_annotation(data)
        return annotation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création: {str(e)}")

@router.get("/{document_id}", response_model=List[Annotation])
async def get_annotations(
    document_id: str,
    page: Optional[int] = Query(None, description="Filtrer par page")
):
    """Récupère toutes les annotations d'un document, optionnellement filtrées par page."""
    annotations = annotation_manager.get_annotations(document_id, page=page)
    return annotations

@router.get("/{document_id}/{annotation_id}", response_model=Annotation)
async def get_annotation(document_id: str, annotation_id: str):
    """Récupère une annotation spécifique."""
    annotation = annotation_manager.get_annotation(document_id, annotation_id)

    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation non trouvée")

    return annotation

@router.put("/{document_id}/{annotation_id}", response_model=Annotation)
async def update_annotation(
    document_id: str,
    annotation_id: str,
    data: AnnotationUpdate
):
    """Met à jour une annotation."""
    annotation = annotation_manager.update_annotation(document_id, annotation_id, data)

    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation non trouvée")

    return annotation

@router.delete("/{document_id}/{annotation_id}")
async def delete_annotation(document_id: str, annotation_id: str):
    """Supprime une annotation."""
    success = annotation_manager.delete_annotation(document_id, annotation_id)

    if not success:
        raise HTTPException(status_code=404, detail="Annotation non trouvée")

    return {"message": "Annotation supprimée avec succès"}

@router.get("/{document_id}/export")
async def export_annotations(document_id: str):
    """Exporte toutes les annotations d'un document au format JSON."""
    export_data = annotation_manager.export_annotations(document_id)
    return export_data
