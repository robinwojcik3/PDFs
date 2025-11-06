"""
Modèles de données pour les annotations.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AnnotationCreate(BaseModel):
    """Données pour créer une annotation."""
    document_id: str
    page: int
    content: str
    annotation_type: str  # "note", "highlight", "comment"
    color: Optional[str] = "#FFFF00"
    position: Optional[dict] = None  # Coordonnées x, y, width, height

class Annotation(BaseModel):
    """Modèle d'annotation complète."""
    id: str
    document_id: str
    page: int
    content: str
    annotation_type: str
    color: str
    position: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

class AnnotationUpdate(BaseModel):
    """Données pour mettre à jour une annotation."""
    content: Optional[str] = None
    color: Optional[str] = None
    position: Optional[dict] = None
