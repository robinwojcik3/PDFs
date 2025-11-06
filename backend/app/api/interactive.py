"""
API endpoints pour les modules pédagogiques interactifs.
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import re
from collections import Counter

router = APIRouter()

# Import du cache des documents
from app.api.documents import documents_cache

@router.get("/{document_id}/concepts")
async def extract_key_concepts(document_id: str):
    """
    Extrait les concepts clés d'un document scientifique.
    Utilise l'analyse de fréquence et les patterns de texte scientifique.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id]

    # Analyser le texte pour extraire les concepts
    text = document.full_text.lower()

    # Mots-clés scientifiques communs à ignorer
    stop_words = {
        'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'à', 'au', 'aux',
        'et', 'ou', 'mais', 'donc', 'or', 'car', 'ni', 'dans', 'par', 'pour',
        'que', 'qui', 'quoi', 'dont', 'où', 'ce', 'ces', 'cet', 'cette',
        'est', 'sont', 'être', 'avoir', 'fait', 'faire', 'peut', 'sont'
    }

    # Extraire les mots significatifs
    words = re.findall(r'\b[a-zàâäéèêëïîôùûü]{4,}\b', text)
    word_freq = Counter([w for w in words if w not in stop_words])

    # Prendre les 20 concepts les plus fréquents
    top_concepts = word_freq.most_common(20)

    # Formater les concepts avec leur fréquence
    concepts = [
        {
            "term": term,
            "frequency": freq,
            "importance": min(100, int((freq / top_concepts[0][1]) * 100)) if top_concepts else 0
        }
        for term, freq in top_concepts
    ]

    return {
        "document_id": document_id,
        "concepts": concepts,
        "keywords": document.metadata.keywords
    }

@router.get("/{document_id}/quiz")
async def generate_quiz(document_id: str):
    """
    Génère un quiz pédagogique basé sur le contenu du document.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id]

    # Générer des questions basées sur les sections et le contenu
    questions = []

    # Question sur le titre et les auteurs
    if document.metadata.title and document.metadata.authors:
        questions.append({
            "id": "q1",
            "type": "multiple_choice",
            "question": f"Qui sont les auteurs de '{document.metadata.title}' ?",
            "options": [
                ", ".join(document.metadata.authors),
                "Auteur inconnu",
                "Plusieurs auteurs anonymes",
                "Non spécifié"
            ],
            "correct_answer": 0,
            "explanation": f"Les auteurs sont: {', '.join(document.metadata.authors)}"
        })

    # Questions sur les sections
    if len(document.sections) > 0:
        questions.append({
            "id": "q2",
            "type": "multiple_choice",
            "question": "Combien de sections principales comporte ce document ?",
            "options": [
                str(len(document.sections)),
                str(len(document.sections) + 2),
                str(max(1, len(document.sections) - 1)),
                str(len(document.sections) * 2)
            ],
            "correct_answer": 0,
            "explanation": f"Le document comporte {len(document.sections)} sections principales."
        })

    # Question sur les figures
    if len(document.figures) > 0:
        questions.append({
            "id": "q3",
            "type": "true_false",
            "question": f"Ce document contient {len(document.figures)} figure(s).",
            "correct_answer": True,
            "explanation": f"Le document contient exactement {len(document.figures)} figure(s)."
        })

    # Question sur les tableaux
    if len(document.tables) > 0:
        questions.append({
            "id": "q4",
            "type": "multiple_choice",
            "question": "Combien de tableaux sont présents dans ce document ?",
            "options": [
                str(len(document.tables)),
                str(len(document.tables) + 1),
                str(max(0, len(document.tables) - 1)),
                "Aucun"
            ],
            "correct_answer": 0,
            "explanation": f"Le document contient {len(document.tables)} tableau(x)."
        })

    return {
        "document_id": document_id,
        "quiz_title": f"Quiz sur: {document.metadata.title or document.filename}",
        "questions": questions,
        "total_questions": len(questions)
    }

@router.get("/{document_id}/summary")
async def generate_summary(document_id: str):
    """
    Génère une fiche de synthèse du document.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id]

    # Créer un résumé structuré
    summary = {
        "title": document.metadata.title or document.filename,
        "authors": document.metadata.authors,
        "year": document.metadata.year,
        "num_pages": document.num_pages,
        "structure": {
            "sections": len(document.sections),
            "figures": len(document.figures),
            "tables": len(document.tables)
        },
        "main_sections": [
            {
                "title": section.title,
                "preview": section.content[:200] + "..." if len(section.content) > 200 else section.content
            }
            for section in document.sections[:5]  # Top 5 sections
        ],
        "keywords": document.metadata.keywords,
        "abstract": document.metadata.abstract
    }

    return summary

@router.get("/{document_id}/statistics")
async def get_document_statistics(document_id: str):
    """
    Génère des statistiques sur le document pour visualisation.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id]

    # Calculer des statistiques
    text = document.full_text
    words = re.findall(r'\b\w+\b', text)

    # Distribution des longueurs de sections
    section_lengths = [len(s.content.split()) for s in document.sections]

    stats = {
        "document_id": document_id,
        "total_words": len(words),
        "total_characters": len(text),
        "avg_words_per_page": len(words) / document.num_pages if document.num_pages > 0 else 0,
        "sections_distribution": [
            {
                "section": section.title,
                "word_count": len(section.content.split()),
                "page_start": section.page_start
            }
            for section in document.sections
        ],
        "visual_elements": {
            "figures": len(document.figures),
            "tables": len(document.tables),
            "figures_per_page": len(document.figures) / document.num_pages if document.num_pages > 0 else 0
        }
    }

    return stats
