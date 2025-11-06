"""
Modèles de données pour les documents PDF.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Figure(BaseModel):
    """Modèle pour une figure extraite."""
    id: str
    page: int
    path: str
    caption: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

class Table(BaseModel):
    """Modèle pour un tableau extrait."""
    id: str
    page: int
    data: List[List[str]]
    caption: Optional[str] = None

class Section(BaseModel):
    """Modèle pour une section du document."""
    id: str
    title: str
    content: str
    page_start: int
    page_end: int
    level: int

class DocumentMetadata(BaseModel):
    """Métadonnées d'un document."""
    title: Optional[str] = None
    authors: List[str] = []
    year: Optional[int] = None
    abstract: Optional[str] = None
    keywords: List[str] = []
    doi: Optional[str] = None

class Document(BaseModel):
    """Modèle complet d'un document PDF indexé."""
    id: str
    filename: str
    path: str
    num_pages: int
    metadata: DocumentMetadata
    sections: List[Section] = []
    figures: List[Figure] = []
    tables: List[Table] = []
    full_text: str
    indexed_at: datetime
    file_size: int

class DocumentSummary(BaseModel):
    """Résumé d'un document pour la liste."""
    id: str
    filename: str
    title: Optional[str]
    authors: List[str]
    year: Optional[int]
    num_pages: int
    num_figures: int
    num_tables: int
    indexed_at: datetime

class SearchResult(BaseModel):
    """Résultat de recherche."""
    document_id: str
    title: str
    filename: str
    score: float
    snippet: str
    page: Optional[int] = None
    highlight: Optional[str] = None
