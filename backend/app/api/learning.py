"""
API endpoints pour les applications pédagogiques interactives.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.services.interactive_generator import InteractiveGenerator

router = APIRouter()

# Import du cache des documents
from app.api.documents import documents_cache

# Initialiser le générateur
interactive_gen = InteractiveGenerator()

@router.get("/{document_id}/interactions")
async def get_all_interactions(document_id: str, include_methodology: bool = True):
    """
    Génère toutes les applications interactives pour un document.

    Crée automatiquement :
    - Visualisations de données
    - Simulations interactives
    - Diagrammes de concepts
    - Exercices pratiques
    - Timelines
    - Calculateurs
    - Explorateurs de graphiques
    - Comparateurs

    Args:
        document_id: ID du document
        include_methodology: Inclure l'analyse méthodologique

    Returns:
        Ensemble complet d'interactions pédagogiques
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id].model_dump()

    # Obtenir l'analyse méthodologique si demandée
    methodology = None
    if include_methodology:
        try:
            from app.services.methodology_analyzer import MethodologyAnalyzer
            analyzer = MethodologyAnalyzer()
            methodology = analyzer.analyze_methodology(document)
        except Exception as e:
            print(f"Erreur analyse méthodologie: {e}")

    # Générer toutes les interactions
    interactions = interactive_gen.generate_all_interactions(document, methodology)

    return interactions

@router.get("/{document_id}/interactions/visualizations")
async def get_visualizations(document_id: str):
    """
    Obtient uniquement les visualisations de données interactives.

    Parfait pour :
    - Explorer les tableaux de résultats
    - Visualiser les distributions
    - Comparer des données
    - Créer des graphiques personnalisés
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id].model_dump()
    interactions = interactive_gen.generate_all_interactions(document)

    visualizations = [
        i for i in interactions['interactions']
        if i['type'] == 'visualization'
    ]

    return {
        "document_id": document_id,
        "visualizations": visualizations,
        "count": len(visualizations)
    }

@router.get("/{document_id}/interactions/simulations")
async def get_simulations(document_id: str):
    """
    Obtient les simulations interactives basées sur le contenu.

    Simulations disponibles :
    - Modèles de croissance (linéaire, exponentiel, logistique)
    - Distributions statistiques (normale, Poisson, etc.)
    - Processus dynamiques (réactions, cinétique)
    - Systèmes d'équations

    Toutes les simulations ont des paramètres ajustables en temps réel.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id].model_dump()
    interactions = interactive_gen.generate_all_interactions(document)

    simulations = [
        i for i in interactions['interactions']
        if i['type'] == 'simulation'
    ]

    return {
        "document_id": document_id,
        "simulations": simulations,
        "count": len(simulations)
    }

@router.get("/{document_id}/interactions/diagrams")
async def get_diagrams(document_id: str):
    """
    Obtient les diagrammes interactifs.

    Types de diagrammes :
    - Cartes mentales de structure
    - Diagrammes de flux méthodologique
    - Réseaux de concepts
    - Graphes de relations

    Tous interactifs avec zoom, pan, recherche, etc.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id].model_dump()
    interactions = interactive_gen.generate_all_interactions(document)

    diagrams = [
        i for i in interactions['interactions']
        if i['type'] == 'diagram'
    ]

    return {
        "document_id": document_id,
        "diagrams": diagrams,
        "count": len(diagrams)
    }

@router.get("/{document_id}/interactions/exercises")
async def get_exercises(document_id: str, difficulty: Optional[str] = Query(None, regex="^(beginner|intermediate|advanced)$")):
    """
    Obtient les exercices pratiques interactifs.

    Types d'exercices :
    - Analyse de données
    - Conception expérimentale
    - Interprétation statistique
    - Résolution de problèmes

    Avec feedback immédiat et hints.

    Args:
        difficulty: Filtrer par difficulté (beginner, intermediate, advanced)
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id].model_dump()

    # Obtenir la méthodologie pour les exercices avancés
    from app.services.methodology_analyzer import MethodologyAnalyzer
    analyzer = MethodologyAnalyzer()
    methodology = analyzer.analyze_methodology(document)

    interactions = interactive_gen.generate_all_interactions(document, methodology)

    exercises = [
        i for i in interactions['interactions']
        if i['type'] == 'exercise'
    ]

    # Filtrer par difficulté si spécifié
    if difficulty:
        exercises = [
            e for e in exercises
            if e.get('config', {}).get('difficulty') == difficulty
        ]

    return {
        "document_id": document_id,
        "exercises": exercises,
        "count": len(exercises),
        "filtered_by": difficulty
    }

@router.get("/{document_id}/interactions/calculators")
async def get_calculators(document_id: str):
    """
    Obtient les calculateurs scientifiques interactifs.

    Calculateurs disponibles :
    - Taille d'échantillon
    - Intervalles de confiance
    - Puissance statistique
    - Taille d'effet
    - Tests statistiques

    Tous avec formules et interprétations.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id].model_dump()
    interactions = interactive_gen.generate_all_interactions(document)

    calculators = [
        i for i in interactions['interactions']
        if i['type'] == 'calculator'
    ]

    return {
        "document_id": document_id,
        "calculators": calculators,
        "count": len(calculators)
    }

@router.get("/{document_id}/interactions/timeline")
async def get_timeline(document_id: str):
    """
    Obtient la timeline interactive de la recherche.

    Affiche chronologiquement :
    - Découvertes mentionnées
    - Dates clés
    - Évolution des concepts
    - Historique de la recherche

    Interactive avec zoom, filtres, et recherche.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id].model_dump()
    interactions = interactive_gen.generate_all_interactions(document)

    timeline = next(
        (i for i in interactions['interactions'] if i['type'] == 'timeline'),
        None
    )

    if not timeline:
        return {
            "document_id": document_id,
            "message": "Aucune timeline disponible pour ce document",
            "timeline": None
        }

    return {
        "document_id": document_id,
        "timeline": timeline
    }

@router.get("/{document_id}/interactions/graph-explorers")
async def get_graph_explorers(document_id: str):
    """
    Obtient les explorateurs de graphiques interactifs.

    Permet d':
    - Explorer les figures du document
    - Mesurer des distances/angles
    - Extraire des points de données
    - Comparer des figures
    - Annoter les images
    - Ajouter des grilles de référence
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id].model_dump()
    interactions = interactive_gen.generate_all_interactions(document)

    explorers = [
        i for i in interactions['interactions']
        if i['type'] == 'graph_explorer'
    ]

    return {
        "document_id": document_id,
        "graph_explorers": explorers,
        "count": len(explorers)
    }

@router.get("/{document_id}/interactions/comparisons")
async def get_comparisons(document_id: str):
    """
    Obtient les comparateurs interactifs.

    Compare :
    - Tableaux de données côte à côte
    - Métriques statistiques
    - Différences visuelles
    - Tendances

    Avec calculs automatiques de différences.
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    document = documents_cache[document_id].model_dump()
    interactions = interactive_gen.generate_all_interactions(document)

    comparisons = [
        i for i in interactions['interactions']
        if i['type'] == 'comparison'
    ]

    return {
        "document_id": document_id,
        "comparisons": comparisons,
        "count": len(comparisons)
    }

@router.get("/types")
async def get_interaction_types():
    """
    Liste tous les types d'interactions disponibles.

    Retourne les descriptions et capacités de chaque type d'interaction.
    """
    return {
        "interaction_types": interactive_gen.interaction_types,
        "total_types": len(interactive_gen.interaction_types)
    }

@router.post("/{document_id}/interactions/custom")
async def create_custom_interaction(
    document_id: str,
    interaction_type: str,
    config: dict
):
    """
    Crée une interaction personnalisée.

    Permet de créer des interactions sur mesure avec des configurations
    spécifiques adaptées aux besoins pédagogiques.

    Args:
        interaction_type: Type d'interaction (visualization, simulation, etc.)
        config: Configuration personnalisée

    Returns:
        Interaction personnalisée créée
    """
    if document_id not in documents_cache:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    if interaction_type not in interactive_gen.interaction_types:
        raise HTTPException(
            status_code=400,
            detail=f"Type d'interaction invalide. Types disponibles : {list(interactive_gen.interaction_types.keys())}"
        )

    custom_interaction = {
        'type': interaction_type,
        'id': f'custom_{interaction_type}',
        'title': config.get('title', f'{interaction_type.title()} personnalisé'),
        'description': config.get('description', ''),
        'config': config,
        'custom': True
    }

    return {
        "document_id": document_id,
        "interaction": custom_interaction,
        "message": "Interaction personnalisée créée"
    }
