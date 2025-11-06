"""
Générateur d'applications interactives pédagogiques pour illustrer les concepts scientifiques.
"""
import re
import json
from typing import List, Dict, Optional, Any
from collections import Counter
import random

class InteractiveGenerator:
    """
    Génère des applications interactives pédagogiques basées sur le contenu des PDFs.
    Crée des simulations, visualisations et exercices pour enseigner les concepts.
    """

    def __init__(self):
        # Types d'interactions disponibles
        self.interaction_types = {
            'visualization': 'Visualisation de données',
            'simulation': 'Simulation interactive',
            'diagram': 'Diagramme interactif',
            'exercise': 'Exercice pratique',
            'quiz_advanced': 'Quiz avancé adaptatif',
            'animation': 'Animation explicative',
            'calculator': 'Calculateur interactif',
            'graph_explorer': 'Explorateur de graphiques',
            'timeline': 'Timeline interactive',
            'comparison': 'Comparateur interactif'
        }

    def generate_all_interactions(self, document: Dict, methodology: Dict = None) -> Dict:
        """
        Génère toutes les applications interactives possibles pour un document.

        Args:
            document: Document scientifique
            methodology: Analyse méthodologique (optionnel)

        Returns:
            Dictionnaire avec toutes les interactions générées
        """
        interactions = {
            'document_id': document.get('id'),
            'title': document.get('metadata', {}).get('title', 'Document'),
            'interactions': []
        }

        # 1. Visualisations de données
        data_viz = self._generate_data_visualizations(document, methodology)
        if data_viz:
            interactions['interactions'].extend(data_viz)

        # 2. Simulations basées sur les équations
        simulations = self._generate_simulations(document)
        if simulations:
            interactions['interactions'].extend(simulations)

        # 3. Diagrammes de concepts
        diagrams = self._generate_concept_diagrams(document)
        if diagrams:
            interactions['interactions'].extend(diagrams)

        # 4. Exercices pratiques
        exercises = self._generate_practical_exercises(document, methodology)
        if exercises:
            interactions['interactions'].extend(exercises)

        # 5. Timeline de recherche
        timeline = self._generate_timeline(document)
        if timeline:
            interactions['interactions'].append(timeline)

        # 6. Calculateurs interactifs
        calculators = self._generate_calculators(document)
        if calculators:
            interactions['interactions'].extend(calculators)

        # 7. Explorateurs de graphiques
        graph_explorers = self._generate_graph_explorers(document)
        if graph_explorers:
            interactions['interactions'].extend(graph_explorers)

        # 8. Comparateurs de concepts
        comparisons = self._generate_comparisons(document)
        if comparisons:
            interactions['interactions'].extend(comparisons)

        return interactions

    def _generate_data_visualizations(self, document: Dict, methodology: Dict) -> List[Dict]:
        """Génère des visualisations de données interactives."""
        visualizations = []

        # Visualisation des tableaux de résultats
        tables = document.get('tables', [])
        for table in tables[:3]:  # Top 3 tableaux
            if len(table.get('data', [])) > 1:
                viz = {
                    'type': 'visualization',
                    'id': f"viz_{table['id']}",
                    'title': f"Visualisation : {table.get('caption', 'Tableau')}",
                    'description': 'Visualisation interactive des données du tableau',
                    'config': {
                        'chart_type': 'bar',  # bar, line, scatter, pie
                        'data': self._extract_numeric_data(table['data']),
                        'interactive_features': [
                            'zoom', 'pan', 'hover_tooltips', 'filter', 'export'
                        ],
                        'customization': {
                            'allow_chart_type_change': True,
                            'allow_color_change': True,
                            'allow_axis_scale': True
                        }
                    }
                }
                visualizations.append(viz)

        # Visualisation de la distribution méthodologique
        if methodology:
            method_viz = {
                'type': 'visualization',
                'id': 'viz_methodology',
                'title': 'Analyse Méthodologique Interactive',
                'description': 'Explorez la méthodologie de recherche de manière interactive',
                'config': {
                    'chart_type': 'radar',
                    'data': {
                        'categories': [
                            'Design Expérimental',
                            'Méthodes Statistiques',
                            'Taille Échantillon',
                            'Validité',
                            'Documentation',
                            'Reproductibilité'
                        ],
                        'values': self._extract_methodology_scores(methodology)
                    },
                    'interactive_features': [
                        'hover_details', 'compare_mode', 'export'
                    ]
                }
            }
            visualizations.append(method_viz)

        return visualizations

    def _generate_simulations(self, document: Dict) -> List[Dict]:
        """Génère des simulations interactives basées sur les équations."""
        simulations = []

        # Détecter les modèles mathématiques
        text = document.get('full_text', '')

        # Simulation pour modèles de croissance
        if any(term in text.lower() for term in ['croissance', 'growth', 'exponentiel', 'exponential']):
            sim = {
                'type': 'simulation',
                'id': 'sim_growth',
                'title': 'Simulateur de Croissance',
                'description': 'Simulez différents modèles de croissance',
                'config': {
                    'model_type': 'growth',
                    'parameters': [
                        {
                            'name': 'rate',
                            'label': 'Taux de croissance',
                            'min': 0,
                            'max': 1,
                            'default': 0.1,
                            'step': 0.01
                        },
                        {
                            'name': 'initial',
                            'label': 'Valeur initiale',
                            'min': 0,
                            'max': 1000,
                            'default': 100,
                            'step': 10
                        },
                        {
                            'name': 'time',
                            'label': 'Durée (temps)',
                            'min': 1,
                            'max': 100,
                            'default': 50,
                            'step': 1
                        }
                    ],
                    'output_type': 'line_chart',
                    'real_time': True,
                    'formulas': [
                        'Linéaire: N(t) = N₀ + rt',
                        'Exponentiel: N(t) = N₀ * e^(rt)',
                        'Logistique: N(t) = K / (1 + ((K-N₀)/N₀) * e^(-rt))'
                    ]
                }
            }
            simulations.append(sim)

        # Simulation pour distributions statistiques
        if any(term in text.lower() for term in ['distribution', 'normale', 'normal', 'gaussian']):
            sim = {
                'type': 'simulation',
                'id': 'sim_distribution',
                'title': 'Explorateur de Distributions',
                'description': 'Explorez différentes distributions statistiques',
                'config': {
                    'model_type': 'distribution',
                    'distributions': ['normal', 'poisson', 'binomial', 'exponential', 't-student'],
                    'parameters': [
                        {
                            'name': 'mean',
                            'label': 'Moyenne (μ)',
                            'min': -10,
                            'max': 10,
                            'default': 0,
                            'step': 0.1
                        },
                        {
                            'name': 'std',
                            'label': 'Écart-type (σ)',
                            'min': 0.1,
                            'max': 5,
                            'default': 1,
                            'step': 0.1
                        },
                        {
                            'name': 'samples',
                            'label': 'Nombre d\'échantillons',
                            'min': 10,
                            'max': 10000,
                            'default': 1000,
                            'step': 100
                        }
                    ],
                    'output_type': 'histogram',
                    'real_time': True,
                    'show_statistics': True
                }
            }
            simulations.append(sim)

        # Simulation pour réactions/processus
        if any(term in text.lower() for term in ['réaction', 'reaction', 'processus', 'process', 'cinétique', 'kinetic']):
            sim = {
                'type': 'simulation',
                'id': 'sim_process',
                'title': 'Simulateur de Processus',
                'description': 'Simulez des processus dynamiques',
                'config': {
                    'model_type': 'process',
                    'parameters': [
                        {
                            'name': 'rate_constant',
                            'label': 'Constante de vitesse (k)',
                            'min': 0.01,
                            'max': 2,
                            'default': 0.5,
                            'step': 0.01
                        },
                        {
                            'name': 'initial_concentration',
                            'label': 'Concentration initiale',
                            'min': 0,
                            'max': 100,
                            'default': 50,
                            'step': 1
                        },
                        {
                            'name': 'temperature',
                            'label': 'Température (°C)',
                            'min': 0,
                            'max': 100,
                            'default': 25,
                            'step': 1
                        }
                    ],
                    'output_type': 'multi_line_chart',
                    'real_time': True,
                    'animation': True
                }
            }
            simulations.append(sim)

        return simulations

    def _generate_concept_diagrams(self, document: Dict) -> List[Dict]:
        """Génère des diagrammes de concepts interactifs."""
        diagrams = []

        sections = document.get('sections', [])

        # Diagramme de structure du document
        if len(sections) > 3:
            diagram = {
                'type': 'diagram',
                'id': 'diagram_structure',
                'title': 'Structure du Document',
                'description': 'Carte mentale interactive de la structure',
                'config': {
                    'diagram_type': 'mindmap',
                    'root': document.get('metadata', {}).get('title', 'Document'),
                    'nodes': [
                        {
                            'id': section.get('id'),
                            'label': section.get('title'),
                            'content_preview': section.get('content', '')[:200],
                            'children': []
                        }
                        for section in sections
                    ],
                    'interactive_features': [
                        'expand_collapse', 'zoom', 'pan', 'search',
                        'click_to_navigate', 'export_svg'
                    ],
                    'styling': {
                        'color_by_level': True,
                        'node_size_by_content': True
                    }
                }
            }
            diagrams.append(diagram)

        # Diagramme de flux méthodologique
        methodology_keywords = ['méthode', 'method', 'protocole', 'protocol', 'étape', 'step']
        has_methodology = any(
            any(kw in section.get('title', '').lower() for kw in methodology_keywords)
            for section in sections
        )

        if has_methodology:
            diagram = {
                'type': 'diagram',
                'id': 'diagram_methodology_flow',
                'title': 'Flux Méthodologique',
                'description': 'Diagramme de flux de la méthodologie',
                'config': {
                    'diagram_type': 'flowchart',
                    'nodes': self._extract_methodology_steps(document),
                    'interactive_features': [
                        'click_for_details', 'zoom', 'highlight_path',
                        'export_svg'
                    ],
                    'styling': {
                        'color_by_type': True,
                        'show_decision_points': True
                    }
                }
            }
            diagrams.append(diagram)

        # Réseau de concepts
        text = document.get('full_text', '')
        words = re.findall(r'\b[a-zàâäéèêëïîôùûü]{5,}\b', text.lower())
        word_freq = Counter(words)
        top_concepts = [word for word, _ in word_freq.most_common(30)]

        if len(top_concepts) >= 10:
            diagram = {
                'type': 'diagram',
                'id': 'diagram_concept_network',
                'title': 'Réseau de Concepts',
                'description': 'Réseau interactif des concepts principaux',
                'config': {
                    'diagram_type': 'network',
                    'nodes': [
                        {'id': concept, 'label': concept, 'size': word_freq[concept]}
                        for concept in top_concepts
                    ],
                    'links': self._generate_concept_links(top_concepts, text),
                    'interactive_features': [
                        'drag_nodes', 'zoom', 'filter_by_frequency',
                        'highlight_connections', 'search', 'cluster_analysis'
                    ],
                    'physics': {
                        'enabled': True,
                        'force_strength': 0.5
                    }
                }
            }
            diagrams.append(diagram)

        return diagrams

    def _generate_practical_exercises(self, document: Dict, methodology: Dict) -> List[Dict]:
        """Génère des exercices pratiques interactifs."""
        exercises = []

        # Exercice d'analyse de données
        tables = document.get('tables', [])
        if tables:
            exercise = {
                'type': 'exercise',
                'id': 'exercise_data_analysis',
                'title': 'Exercice : Analyse de Données',
                'description': 'Analysez les données du tableau et tirez des conclusions',
                'config': {
                    'exercise_type': 'data_analysis',
                    'difficulty': 'intermediate',
                    'data': tables[0].get('data', []),
                    'tasks': [
                        {
                            'task': 'Identifiez la tendance générale',
                            'type': 'multiple_choice',
                            'options': ['Croissance', 'Décroissance', 'Stable', 'Cyclique'],
                            'hint': 'Observez l\'évolution des valeurs'
                        },
                        {
                            'task': 'Calculez la moyenne des valeurs',
                            'type': 'numeric_input',
                            'tolerance': 0.01,
                            'hint': 'Somme / Nombre de valeurs'
                        },
                        {
                            'task': 'Identifiez les valeurs aberrantes',
                            'type': 'selection',
                            'hint': 'Cherchez les valeurs très éloignées de la moyenne'
                        }
                    ],
                    'feedback': {
                        'immediate': True,
                        'show_solution': True,
                        'hints_available': 3
                    }
                }
            }
            exercises.append(exercise)

        # Exercice de conception expérimentale
        if methodology:
            exercise = {
                'type': 'exercise',
                'id': 'exercise_experimental_design',
                'title': 'Exercice : Conception Expérimentale',
                'description': 'Concevez une expérience similaire',
                'config': {
                    'exercise_type': 'design',
                    'difficulty': 'advanced',
                    'scenario': self._extract_research_context(document),
                    'tasks': [
                        {
                            'task': 'Définissez l\'hypothèse de recherche',
                            'type': 'text_input',
                            'validation': 'contains_hypothesis_structure'
                        },
                        {
                            'task': 'Choisissez le design expérimental approprié',
                            'type': 'multiple_choice',
                            'options': [
                                'Essai contrôlé randomisé',
                                'Étude observationnelle',
                                'Étude de cohorte',
                                'Étude cas-témoin'
                            ]
                        },
                        {
                            'task': 'Identifiez les variables dépendantes et indépendantes',
                            'type': 'drag_drop',
                            'categories': ['Variable indépendante', 'Variable dépendante', 'Variable contrôle']
                        },
                        {
                            'task': 'Calculez la taille d\'échantillon nécessaire',
                            'type': 'calculator',
                            'formula': 'power_analysis'
                        }
                    ],
                    'feedback': {
                        'immediate': True,
                        'expert_guidance': True
                    }
                }
            }
            exercises.append(exercise)

        # Exercice d'interprétation statistique
        if any(term in document.get('full_text', '').lower() for term in ['p-value', 'significatif', 'significant']):
            exercise = {
                'type': 'exercise',
                'id': 'exercise_statistical_interpretation',
                'title': 'Exercice : Interprétation Statistique',
                'description': 'Interprétez les résultats statistiques',
                'config': {
                    'exercise_type': 'interpretation',
                    'difficulty': 'intermediate',
                    'scenario': {
                        'test': 't-test',
                        'p_value': random.uniform(0.001, 0.1),
                        'effect_size': random.uniform(0.2, 0.8),
                        'sample_size': random.randint(30, 200),
                        'context': 'Comparaison de deux groupes'
                    },
                    'tasks': [
                        {
                            'task': 'Le résultat est-il statistiquement significatif (α=0.05)?',
                            'type': 'true_false',
                            'explanation_required': True
                        },
                        {
                            'task': 'Quelle est la taille de l\'effet?',
                            'type': 'multiple_choice',
                            'options': ['Petit', 'Moyen', 'Grand']
                        },
                        {
                            'task': 'Rédigez une interprétation complète',
                            'type': 'text_input',
                            'min_words': 50,
                            'validation': 'check_interpretation_quality'
                        }
                    ]
                }
            }
            exercises.append(exercise)

        return exercises

    def _generate_timeline(self, document: Dict) -> Optional[Dict]:
        """Génère une timeline interactive de la recherche."""
        metadata = document.get('metadata', {})
        sections = document.get('sections', [])

        # Extraire les dates et événements
        text = document.get('full_text', '')
        year_pattern = r'\b(19|20)\d{2}\b'
        years = list(set(re.findall(year_pattern, text)))

        if len(years) >= 3:
            timeline = {
                'type': 'timeline',
                'id': 'timeline_research',
                'title': 'Timeline de la Recherche',
                'description': 'Chronologie interactive des événements et découvertes',
                'config': {
                    'start_year': min(int(y) for y in years),
                    'end_year': max(int(y) for y in years),
                    'events': self._extract_timeline_events(text, years),
                    'interactive_features': [
                        'zoom_time_range',
                        'click_for_details',
                        'filter_by_category',
                        'search',
                        'export_timeline'
                    ],
                    'visualization': {
                        'type': 'horizontal',
                        'show_connections': True,
                        'color_by_category': True
                    }
                }
            }
            return timeline

        return None

    def _generate_calculators(self, document: Dict) -> List[Dict]:
        """Génère des calculateurs interactifs."""
        calculators = []

        text = document.get('full_text', '').lower()

        # Calculateur de taille d'échantillon
        if any(term in text for term in ['échantillon', 'sample', 'power', 'puissance']):
            calc = {
                'type': 'calculator',
                'id': 'calc_sample_size',
                'title': 'Calculateur de Taille d\'Échantillon',
                'description': 'Calculez la taille d\'échantillon nécessaire',
                'config': {
                    'calculator_type': 'sample_size',
                    'inputs': [
                        {'name': 'effect_size', 'label': 'Taille d\'effet', 'type': 'number', 'min': 0.1, 'max': 2, 'default': 0.5},
                        {'name': 'alpha', 'label': 'Niveau alpha (α)', 'type': 'number', 'min': 0.01, 'max': 0.1, 'default': 0.05},
                        {'name': 'power', 'label': 'Puissance (1-β)', 'type': 'number', 'min': 0.7, 'max': 0.99, 'default': 0.8},
                        {'name': 'groups', 'label': 'Nombre de groupes', 'type': 'integer', 'min': 1, 'max': 10, 'default': 2}
                    ],
                    'formula': 'sample_size_calculation',
                    'output_format': {
                        'type': 'detailed',
                        'show_interpretation': True,
                        'show_confidence_interval': True
                    }
                }
            }
            calculators.append(calc)

        # Calculateur d'intervalle de confiance
        if 'confiance' in text or 'confidence' in text:
            calc = {
                'type': 'calculator',
                'id': 'calc_confidence_interval',
                'title': 'Calculateur d\'Intervalle de Confiance',
                'description': 'Calculez les intervalles de confiance',
                'config': {
                    'calculator_type': 'confidence_interval',
                    'inputs': [
                        {'name': 'mean', 'label': 'Moyenne', 'type': 'number'},
                        {'name': 'std', 'label': 'Écart-type', 'type': 'number', 'min': 0},
                        {'name': 'n', 'label': 'Taille échantillon', 'type': 'integer', 'min': 2},
                        {'name': 'confidence', 'label': 'Niveau de confiance (%)', 'type': 'number', 'min': 90, 'max': 99, 'default': 95}
                    ],
                    'formula': 'confidence_interval_calculation',
                    'visualization': {
                        'type': 'bell_curve',
                        'show_ci_region': True
                    }
                }
            }
            calculators.append(calc)

        return calculators

    def _generate_graph_explorers(self, document: Dict) -> List[Dict]:
        """Génère des explorateurs de graphiques interactifs."""
        explorers = []

        figures = document.get('figures', [])

        # Explorateur de graphiques scientifiques
        if len(figures) >= 2:
            explorer = {
                'type': 'graph_explorer',
                'id': 'explorer_figures',
                'title': 'Explorateur de Figures',
                'description': 'Explorez les figures du document de manière interactive',
                'config': {
                    'figures': [
                        {
                            'id': fig.get('id'),
                            'path': fig.get('path'),
                            'caption': fig.get('caption'),
                            'page': fig.get('page'),
                            'annotations_enabled': True
                        }
                        for fig in figures
                    ],
                    'interactive_features': [
                        'zoom_pan',
                        'measure_tool',
                        'color_picker',
                        'annotation',
                        'compare_figures',
                        'extract_data_points',
                        'overlay_grid'
                    ],
                    'tools': {
                        'measurement': True,
                        'data_extraction': True,
                        'comparison': True
                    }
                }
            }
            explorers.append(explorer)

        return explorers

    def _generate_comparisons(self, document: Dict) -> List[Dict]:
        """Génère des comparateurs interactifs."""
        comparisons = []

        tables = document.get('tables', [])

        # Comparateur de données
        if len(tables) >= 2:
            comparison = {
                'type': 'comparison',
                'id': 'compare_tables',
                'title': 'Comparateur de Données',
                'description': 'Comparez les tableaux de données côte à côte',
                'config': {
                    'items': [
                        {
                            'id': table.get('id'),
                            'label': table.get('caption', f"Tableau {i+1}"),
                            'data': table.get('data')
                        }
                        for i, table in enumerate(tables[:4])
                    ],
                    'comparison_mode': 'side_by_side',
                    'interactive_features': [
                        'highlight_differences',
                        'statistical_comparison',
                        'visual_comparison',
                        'export_comparison'
                    ],
                    'metrics': ['mean', 'median', 'std', 'range']
                }
            }
            comparisons.append(comparison)

        return comparisons

    # Helper methods

    def _extract_numeric_data(self, table_data: List[List[str]]) -> Dict:
        """Extrait les données numériques d'un tableau."""
        if not table_data or len(table_data) < 2:
            return {'labels': [], 'values': []}

        headers = table_data[0]
        data = {'labels': [], 'datasets': []}

        # Essayer d'extraire les nombres
        for row in table_data[1:]:
            if row:
                data['labels'].append(str(row[0]))

        # Extraire les valeurs numériques
        for col_idx in range(1, len(headers)):
            values = []
            for row in table_data[1:]:
                if col_idx < len(row):
                    try:
                        val = float(re.sub(r'[^\d.-]', '', str(row[col_idx])))
                        values.append(val)
                    except:
                        values.append(0)

            if values:
                data['datasets'].append({
                    'label': headers[col_idx] if col_idx < len(headers) else f'Série {col_idx}',
                    'data': values
                })

        return data

    def _extract_methodology_scores(self, methodology: Dict) -> List[float]:
        """Extrait les scores pour le radar de méthodologie."""
        analysis = methodology.get('methodology_analysis', {})

        scores = []

        # Design expérimental
        design_features = len(analysis.get('experimental_design', {}).get('features', {}))
        scores.append(min(100, design_features * 20))

        # Méthodes statistiques
        stat_methods = len(analysis.get('statistical_methods', []))
        scores.append(min(100, stat_methods * 15))

        # Taille échantillon
        sample_size = analysis.get('sample_info', {}).get('size')
        if sample_size:
            scores.append(min(100, (sample_size / 100) * 100))
        else:
            scores.append(0)

        # Validité
        validity = analysis.get('validity_indicators', {})
        validity_score = sum(1 for v in validity.values() if v) * 20
        scores.append(validity_score)

        # Documentation
        has_methodology = 1 if analysis.get('methodology_section') else 0
        scores.append(has_methodology * 100)

        # Reproductibilité
        protocol_steps = len(analysis.get('protocol_steps', []))
        scores.append(min(100, protocol_steps * 10))

        return scores

    def _extract_methodology_steps(self, document: Dict) -> List[Dict]:
        """Extrait les étapes méthodologiques pour un flowchart."""
        steps = []

        sections = document.get('sections', [])
        methodology_section = None

        for section in sections:
            if any(kw in section.get('title', '').lower() for kw in ['méthode', 'method', 'protocole']):
                methodology_section = section
                break

        if methodology_section:
            content = methodology_section.get('content', '')
            lines = content.split('\n')

            step_num = 0
            for line in lines:
                line = line.strip()

                # Détecter les étapes
                if re.match(r'^(\d+[\.\)]|\-|\*)', line) or any(kw in line.lower() for kw in ['étape', 'step', 'ensuite', 'puis']):
                    step_num += 1
                    steps.append({
                        'id': f'step_{step_num}',
                        'label': f'Étape {step_num}',
                        'description': line[:100],
                        'type': 'process'
                    })

        return steps[:10]  # Max 10 étapes

    def _generate_concept_links(self, concepts: List[str], text: str) -> List[Dict]:
        """Génère les liens entre concepts."""
        links = []

        # Rechercher les cooccurrences
        for i, concept1 in enumerate(concepts):
            for concept2 in concepts[i+1:]:
                # Vérifier si les concepts apparaissent proches dans le texte
                pattern = f'{concept1}.{{0,50}}{concept2}|{concept2}.{{0,50}}{concept1}'
                matches = re.findall(pattern, text.lower())

                if len(matches) > 2:
                    links.append({
                        'source': concept1,
                        'target': concept2,
                        'strength': min(len(matches), 10)
                    })

        return links[:50]  # Max 50 liens

    def _extract_research_context(self, document: Dict) -> str:
        """Extrait le contexte de recherche."""
        metadata = document.get('metadata', {})
        abstract = metadata.get('abstract', '')

        if abstract:
            return abstract[:300]

        # Sinon, utiliser le début du texte
        text = document.get('full_text', '')
        return text[:300]

    def _extract_timeline_events(self, text: str, years: List[str]) -> List[Dict]:
        """Extrait les événements pour la timeline."""
        events = []

        for year in sorted(set(years)):
            # Trouver les phrases contenant l'année
            pattern = f'.{{0,100}}{year}.{{0,100}}'
            matches = re.findall(pattern, text)

            if matches:
                events.append({
                    'year': int(year),
                    'title': f'Événement en {year}',
                    'description': matches[0].strip(),
                    'category': 'research'
                })

        return events[:20]  # Max 20 événements
