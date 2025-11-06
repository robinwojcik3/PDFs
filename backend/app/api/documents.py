"""
API endpoints pour la gestion des documents PDF.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import os

from app.models.document import Document, DocumentSummary
from app.services.pdf_processor import PDFProcessor
from app.services.search_indexer import SearchIndexer

router = APIRouter()

# Initialiser les services
pdf_processor = PDFProcessor()
search_indexer = SearchIndexer()

# Cache en mémoire des documents (pour démo, utiliser une vraie DB en production)
documents_cache = {}

@router.get("/", response_model=List[DocumentSummary])
async def list_documents():
    """Liste tous les documents indexés."""
    summaries = []

    for doc_id, doc in documents_cache.items():
        summaries.append(DocumentSummary(
            id=doc.id,
            filename=doc.filename,
            title=doc.metadata.title,
            authors=doc.metadata.authors,
            year=doc.metadata.year,
            num_pages=doc.num_pages,
            num_figures=len(doc.figures),
            num_tables=len(doc.tables),
            indexed_at=doc.indexed_at
        ))

    return summaries

@router.get("/{document_id}", response_model=Document)
async def get_document(document_id: str):
    """Récupère un document spécifique par son ID."""
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    return documents_cache[document_id]

@router.post("/index")
async def index_documents(background_tasks: BackgroundTasks):
    """
    Indexe tous les PDFs du dossier.
    Lance le traitement en arrière-plan pour ne pas bloquer.
    """
    pdfs = pdf_processor.list_pdfs()

    if not pdfs:
        return {
            "message": "Aucun PDF trouvé dans le dossier",
            "path": pdf_processor.pdf_dir
        }

    # Lancer l'indexation en arrière-plan
    background_tasks.add_task(index_all_pdfs, pdfs)

    return {
        "message": f"Indexation de {len(pdfs)} PDF(s) lancée",
        "files": pdfs
    }

@router.post("/index/{filename}")
async def index_single_document(filename: str):
    """Indexe un seul document PDF."""
    try:
        # Traiter le PDF
        document = pdf_processor.process_pdf(filename)

        # Sauvegarder en cache
        documents_cache[document.id] = document

        # Indexer pour la recherche
        search_indexer.index_document(document)

        return {
            "message": f"Document '{filename}' indexé avec succès",
            "document_id": document.id,
            "num_pages": document.num_pages,
            "num_figures": len(document.figures),
            "num_tables": len(document.tables)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'indexation: {str(e)}")

@router.get("/{document_id}/sections")
async def get_document_sections(document_id: str):
    """Récupère toutes les sections d'un document."""
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    return documents_cache[document_id].sections

@router.get("/{document_id}/figures")
async def get_document_figures(document_id: str):
    """Récupère toutes les figures d'un document."""
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    return documents_cache[document_id].figures

@router.get("/{document_id}/tables")
async def get_document_tables(document_id: str):
    """Récupère tous les tableaux d'un document."""
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    return documents_cache[document_id].tables

def index_all_pdfs(pdfs: List[str]):
    """Fonction helper pour indexer tous les PDFs en arrière-plan."""
    for pdf_file in pdfs:
        try:
            document = pdf_processor.process_pdf(pdf_file)
            documents_cache[document.id] = document
            search_indexer.index_document(document)
            print(f"✓ Indexé: {pdf_file}")
        except Exception as e:
            print(f"✗ Erreur avec {pdf_file}: {e}")
