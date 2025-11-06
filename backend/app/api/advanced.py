"""
API endpoints pour les fonctionnalités avancées de recherche scientifique.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.services.bibliography_extractor import BibliographyExtractor
from app.services.equation_detector import EquationDetector
from app.services.methodology_analyzer import MethodologyAnalyzer
from app.services.document_comparator import DocumentComparator
from app.services.recommender import DocumentRecommender
from app.services.exporter import DocumentExporter

router = APIRouter()

# Import du cache des documents
from app.api.documents import documents_cache

# Initialiser les services
bibliography_extractor = BibliographyExtractor()
equation_detector = EquationDetector()
methodology_analyzer = MethodologyAnalyzer()
document_comparator = DocumentComparator()
exporter = DocumentExporter()

@router.get("/{document_id}/bibliography")
async def extract_bibliography(document_id: str):
    """
    Extrait la bibliographie complète d'un document.

    Identifie les références citées dans le texte et la section bibliographie.
    Utile pour l'analyse de citations et la construction de réseaux de connaissances.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id]

    # Extraire les citations
    citations = bibliography_extractor.extract_citations(document.full_text)

    # Extraire la bibliographie
    references = bibliography_extractor.extract_bibliography(document.full_text)

    # Statistiques
    stats = bibliography_extractor.get_citation_statistics(citations)

    return {
        "document_id": document_id,
        "citations": citations,
        "references": references,
        "statistics": stats,
        "total_citations": len(citations),
        "total_references": len(references)
    }

@router.get("/{document_id}/bibliography/export")
async def export_bibliography(
    document_id: str,
    format: str = Query("bibtex", regex="^(bibtex|ris|json)$")
):
    """
    Exporte la bibliographie dans différents formats (BibTeX, RIS, JSON).

    Formats supportés:
    - bibtex: Pour LaTeX et gestionnaires de références
    - ris: Pour EndNote et autres
    - json: Format structuré
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id]
    references = bibliography_extractor.extract_bibliography(document.full_text)

    if format == "bibtex":
        content = bibliography_extractor.export_to_bibtex(references)
    elif format == "ris":
        content = exporter.export_citations(references, format='ris')
    else:
        content = exporter.export_citations(references, format='json')

    return {
        "document_id": document_id,
        "format": format,
        "content": content,
        "reference_count": len(references)
    }

@router.get("/{document_id}/equations")
async def detect_equations(document_id: str):
    """
    Détecte et extrait toutes les équations mathématiques du document.

    Identifie:
    - Équations LaTeX (inline et display)
    - Formules avec symboles mathématiques
    - Variables et opérateurs utilisés

    Utile pour l'analyse de modèles mathématiques et la compréhension des formulations théoriques.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id]

    # Détecter les équations
    equations = equation_detector.detect_equations(document.full_text)

    # Statistiques
    stats = equation_detector.get_equation_statistics(equations)

    return {
        "document_id": document_id,
        "equations": equations,
        "statistics": stats,
        "total_equations": len(equations)
    }

@router.get("/{document_id}/methodology")
async def analyze_methodology(document_id: str):
    """
    Analyse la méthodologie scientifique de l'article.

    Extrait et analyse:
    - Type d'approche (quantitative, qualitative, mixte)
    - Méthodes utilisées
    - Design expérimental
    - Outils et logiciels
    - Protocole et étapes
    - Score de rigueur méthodologique

    Essentiel pour évaluer la qualité scientifique et la reproductibilité de la recherche.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id]

    # Analyser la méthodologie
    analysis = methodology_analyzer.analyze_methodology(document.model_dump())

    return {
        "document_id": document_id,
        "methodology_analysis": analysis
    }

@router.post("/compare")
async def compare_documents(document_ids: List[str]):
    """
    Compare plusieurs documents scientifiques entre eux.

    Analyse:
    - Similarité de contenu
    - Auteurs communs
    - Mots-clés partagés
    - Structure comparative
    - Clusters de documents similaires

    Permet d'identifier des groupes thématiques et des connexions entre recherches.
    """
    if len(document_ids) < 2:
        raise HTTPException(status_code=400, detail="Au moins 2 documents requis")

    # Vérifier que tous les documents existent
    documents = []
    for doc_id in document_ids:
        if doc_id not in documents_cache:
            raise HTTPException(status_code=404, detail=f"Document {doc_id} non trouvé")
        documents.append(documents_cache[doc_id].model_dump())

    if len(documents) == 2:
        # Comparaison de 2 documents
        comparison = document_comparator.compare_documents(documents[0], documents[1])
        return {
            "comparison_type": "pairwise",
            "document_ids": document_ids,
            "comparison": comparison
        }
    else:
        # Comparaison multiple
        comparison = document_comparator.compare_multiple(documents)
        return {
            "comparison_type": "multiple",
            "document_ids": document_ids,
            "comparison": comparison
        }

@router.get("/{document_id}/recommendations")
async def get_recommendations(
    document_id: str,
    limit: int = Query(5, ge=1, le=20)
):
    """
    Recommande des documents similaires ou connexes.

    Basé sur:
    - Similarité de contenu
    - Auteurs communs
    - Mots-clés partagés
    - Thématiques proches

    Aide à la découverte de littérature pertinente et à l'exploration de domaines connexes.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    recommender = DocumentRecommender(documents_cache)

    recommendations = recommender.recommend_similar(
        document_id=document_id,
        limit=limit
    )

    return {
        "document_id": document_id,
        "recommendations": recommendations,
        "count": len(recommendations)
    }

@router.get("/recommendations/by-topic")
async def recommend_by_topic(
    keywords: List[str] = Query(...),
    limit: int = Query(5, ge=1, le=20)
):
    """
    Recommande des documents par thématique/mots-clés.

    Utile pour explorer un domaine spécifique ou trouver des ressources
    sur un sujet donné.
    """
    recommender = DocumentRecommender(documents_cache)

    recommendations = recommender.recommend_by_topic(
        keywords=keywords,
        limit=limit
    )

    return {
        "keywords": keywords,
        "recommendations": recommendations,
        "count": len(recommendations)
    }

@router.get("/recommendations/trending-topics")
async def get_trending_topics(limit: int = Query(10, ge=1, le=50)):
    """
    Identifie les sujets tendances dans la collection de documents.

    Basé sur la fréquence des mots-clés dans les documents indexés.
    Aide à identifier les domaines de recherche actifs.
    """
    recommender = DocumentRecommender(documents_cache)

    trending = recommender.get_trending_topics(limit=limit)

    return {
        "trending_topics": trending,
        "count": len(trending)
    }

@router.get("/network/authors")
async def get_author_network():
    """
    Génère un réseau de collaborations entre auteurs.

    Identifie:
    - Auteurs les plus prolifiques
    - Collaborations fréquentes
    - Réseaux de recherche

    Utile pour l'analyse bibliométrique et l'identification d'experts.
    """
    recommender = DocumentRecommender(documents_cache)

    network = recommender.get_author_network()

    return network

@router.get("/{document_id}/export")
async def export_document(
    document_id: str,
    format: str = Query("markdown", regex="^(markdown|latex|json|html)$"),
    include_annotations: bool = Query(True)
):
    """
    Exporte un document dans différents formats.

    Formats supportés:
    - markdown: Format Markdown avec structure
    - latex: Document LaTeX compilable
    - json: Export structuré complet
    - html: Fiche de synthèse HTML

    Permet la réutilisation et le partage des documents analysés.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id]

    # Récupérer les annotations si demandé
    annotations = []
    if include_annotations:
        from app.services.annotation_manager import AnnotationManager
        annotation_manager = AnnotationManager()
        annotations = annotation_manager.get_annotations(document_id)
        annotations = [a.model_dump() for a in annotations]

    # Exporter selon le format
    if format == "markdown":
        content = exporter.export_to_markdown(
            document.model_dump(),
            include_annotations=include_annotations,
            annotations=annotations
        )
    elif format == "latex":
        content = exporter.export_to_latex(document.model_dump())
    elif format == "json":
        content = exporter.export_to_json(
            document.model_dump(),
            include_annotations=include_annotations,
            annotations=annotations
        )
    else:  # html
        content = exporter.export_summary_to_pdf_html(document.model_dump())

    return {
        "document_id": document_id,
        "format": format,
        "content": content,
        "filename": f"{document.filename.replace('.pdf', '')}.{format}"
    }

@router.get("/statistics/global")
async def get_global_statistics():
    """
    Statistiques globales sur la collection de documents.

    Fournit une vue d'ensemble de la bibliothèque scientifique indexée.
    """
    total_docs = len(documents_cache)

    if total_docs == 0:
        return {
            "total_documents": 0,
            "message": "Aucun document indexé"
        }

    # Statistiques générales
    total_pages = sum(doc.num_pages for doc in documents_cache.values())
    total_figures = sum(len(doc.figures) for doc in documents_cache.values())
    total_tables = sum(len(doc.tables) for doc in documents_cache.values())
    total_sections = sum(len(doc.sections) for doc in documents_cache.values())

    # Distribution par année
    years = [doc.metadata.year for doc in documents_cache.values() if doc.metadata.year]
    year_distribution = {}
    for year in years:
        year_distribution[year] = year_distribution.get(year, 0) + 1

    # Auteurs les plus fréquents
    all_authors = []
    for doc in documents_cache.values():
        all_authors.extend(doc.metadata.authors)

    from collections import Counter
    author_counts = Counter(all_authors)

    return {
        "total_documents": total_docs,
        "total_pages": total_pages,
        "total_figures": total_figures,
        "total_tables": total_tables,
        "total_sections": total_sections,
        "average_pages_per_document": round(total_pages / total_docs, 1),
        "average_figures_per_document": round(total_figures / total_docs, 1),
        "year_distribution": dict(sorted(year_distribution.items())),
        "top_authors": [
            {"author": author, "documents": count}
            for author, count in author_counts.most_common(10)
        ]
    }
