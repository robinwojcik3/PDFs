"""
Analyseur de méthodologie scientifique dans les articles.
Service d'extraction et d'analyse des protocoles, méthodes et approches expérimentales.
"""
import re
from typing import List, Dict, Optional
from collections import defaultdict

class MethodologyAnalyzer:
    """
    Analyse la méthodologie scientifique des articles de recherche.
    Extrait les protocoles, méthodes, outils, et approches expérimentales.
    """

    def __init__(self):
        # Sections méthodologiques courantes
        self.methodology_keywords = [
            'méthodologie', 'methodology', 'méthodes', 'methods',
            'matériel et méthodes', 'materials and methods',
            'protocole', 'protocol', 'procédure', 'procedure',
            'approche expérimentale', 'experimental approach',
            'design expérimental', 'experimental design',
            'dispositif expérimental', 'experimental setup'
        ]

        # Indicateurs de méthodes quantitatives
        self.quantitative_indicators = [
            'analyse statistique', 'statistical analysis',
            'régression', 'regression', 'corrélation', 'correlation',
            'anova', 't-test', 'test-t', 'chi-square', 'khi-deux',
            'modèle linéaire', 'linear model',
            'significance', 'significatif', 'p-value', 'valeur-p',
            'interval de confiance', 'confidence interval',
            'échantillon', 'sample', 'population',
            'randomisation', 'randomization'
        ]

        # Indicateurs de méthodes qualitatives
        self.qualitative_indicators = [
            'entretien', 'interview', 'focus group',
            'observation', 'ethnograph',
            'analyse thématique', 'thematic analysis',
            'codage', 'coding', 'catégorisation',
            'grounded theory', 'théorie ancrée',
            'phénoménologie', 'phenomenology',
            'étude de cas', 'case study'
        ]

        # Outils et technologies
        self.tools_patterns = [
            r'(?:utilisant|using|avec|with)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)',
            r'logiciel\s+([A-Z][a-zA-Z]+)',
            r'software\s+([A-Z][a-zA-Z]+)',
            r'package\s+([a-zA-Z]+)',
            r'(?:Python|R|MATLAB|SPSS|Excel|Stata)\s*(?:version\s+[\d.]+)?'
        ]

        # Protocoles expérimentaux
        self.protocol_indicators = [
            'étape', 'step', 'phase',
            'procédure suivante', 'following procedure',
            'protocole standard', 'standard protocol',
            'conditions expérimentales', 'experimental conditions'
        ]

    def analyze_methodology(self, document: Dict) -> Dict:
        """
        Analyse complète de la méthodologie d'un document.

        Args:
            document: Document à analyser

        Returns:
            Analyse méthodologique complète
        """
        full_text = document.get('full_text', '')
        sections = document.get('sections', [])

        # Identifier la section méthodologie
        methodology_section = self._find_methodology_section(sections)

        analysis = {
            'methodology_section': methodology_section,
            'approach_type': self._detect_approach_type(full_text, methodology_section),
            'methods_used': self._extract_methods(full_text, methodology_section),
            'tools_and_software': self._extract_tools(full_text, methodology_section),
            'statistical_methods': self._extract_statistical_methods(full_text),
            'experimental_design': self._analyze_experimental_design(full_text, methodology_section),
            'data_collection': self._extract_data_collection_info(full_text, methodology_section),
            'sample_info': self._extract_sample_info(full_text),
            'protocol_steps': self._extract_protocol_steps(methodology_section),
            'validity_indicators': self._assess_validity(full_text),
            'rigor_score': 0.0
        }

        # Calculer un score de rigueur méthodologique
        analysis['rigor_score'] = self._calculate_rigor_score(analysis)

        return analysis

    def _find_methodology_section(self, sections: List[Dict]) -> Optional[Dict]:
        """Trouve la section méthodologie."""
        for section in sections:
            title_lower = section.get('title', '').lower()

            if any(keyword in title_lower for keyword in self.methodology_keywords):
                return section

        return None

    def _detect_approach_type(self, text: str, methodology_section: Optional[Dict]) -> Dict:
        """
        Détecte le type d'approche de recherche.

        Returns:
            Type d'approche avec scores de confiance
        """
        search_text = methodology_section['content'] if methodology_section else text
        search_text_lower = search_text.lower()

        quant_score = sum(1 for indicator in self.quantitative_indicators if indicator in search_text_lower)
        qual_score = sum(1 for indicator in self.qualitative_indicators if indicator in search_text_lower)

        # Détecter les approches spécifiques
        approaches = {
            'quantitative': quant_score > 0,
            'qualitative': qual_score > 0,
            'mixte': quant_score > 0 and qual_score > 0,
            'experimental': any(term in search_text_lower for term in [
                'expérience', 'experiment', 'essai contrôlé', 'controlled trial',
                'randomisé', 'randomized', 'groupe témoin', 'control group'
            ]),
            'observationnel': any(term in search_text_lower for term in [
                'observationnel', 'observational', 'étude de cohorte', 'cohort study',
                'étude transversale', 'cross-sectional'
            ]),
            'computationnel': any(term in search_text_lower for term in [
                'simulation', 'modélisation', 'modeling', 'algorithme', 'algorithm',
                'computationnel', 'computational'
            ])
        }

        # Type principal
        if approaches['mixte']:
            main_type = 'Approche mixte (quantitative et qualitative)'
        elif quant_score > qual_score:
            main_type = 'Approche quantitative'
        elif qual_score > quant_score:
            main_type = 'Approche qualitative'
        else:
            main_type = 'Approche non spécifiée'

        return {
            'main_type': main_type,
            'approaches': {k: v for k, v in approaches.items() if v},
            'quantitative_indicators_count': quant_score,
            'qualitative_indicators_count': qual_score
        }

    def _extract_methods(self, text: str, methodology_section: Optional[Dict]) -> List[Dict]:
        """Extrait les méthodes utilisées."""
        search_text = methodology_section['content'] if methodology_section else text

        methods = []

        # Recherche de patterns de méthodes
        method_patterns = [
            r'(?:méthode|method)(?:\s+de)?\s+([a-zA-Zéèêà\s]+)',
            r'(?:analyse|analysis)\s+([a-zA-Zéèêà\s]+)',
            r'(?:technique|technique)\s+(?:de|d\')?\s*([a-zA-Zéèêà\s]+)',
            r'(?:approche|approach)\s+([a-zA-Zéèêà\s]+)'
        ]

        for pattern in method_patterns:
            matches = re.finditer(pattern, search_text, re.IGNORECASE)

            for match in matches:
                method_name = match.group(1).strip()

                # Filtrer les matches trop courts ou génériques
                if len(method_name) > 5 and method_name.lower() not in ['générale', 'general', 'standard']:
                    methods.append({
                        'name': method_name,
                        'type': self._classify_method(method_name),
                        'context': search_text[max(0, match.start()-100):min(len(search_text), match.end()+100)]
                    })

        # Dédupliquer
        seen = set()
        unique_methods = []

        for method in methods:
            name_lower = method['name'].lower()
            if name_lower not in seen:
                seen.add(name_lower)
                unique_methods.append(method)

        return unique_methods[:15]  # Limiter à 15

    def _extract_tools(self, text: str, methodology_section: Optional[Dict]) -> List[Dict]:
        """Extrait les outils et logiciels utilisés."""
        search_text = methodology_section['content'] if methodology_section else text

        tools = []
        seen = set()

        for pattern in self.tools_patterns:
            matches = re.finditer(pattern, search_text, re.IGNORECASE)

            for match in matches:
                tool_name = match.group(0).strip()

                if tool_name.lower() not in seen and len(tool_name) > 2:
                    seen.add(tool_name.lower())

                    tools.append({
                        'name': tool_name,
                        'category': self._classify_tool(tool_name)
                    })

        return tools

    def _extract_statistical_methods(self, text: str) -> List[Dict]:
        """Extrait les méthodes statistiques mentionnées."""
        statistical_tests = {
            't-test': ['t-test', 'test-t', 'student'],
            'ANOVA': ['anova', 'analyse de variance'],
            'Chi-square': ['chi-square', 'khi-deux', 'χ²'],
            'Régression': ['régression', 'regression'],
            'Corrélation': ['corrélation', 'correlation', 'pearson', 'spearman'],
            'Mann-Whitney': ['mann-whitney', 'u-test'],
            'Wilcoxon': ['wilcoxon'],
            'Kruskal-Wallis': ['kruskal-wallis'],
            'Post-hoc': ['post-hoc', 'tukey', 'bonferroni'],
            'Modèle mixte': ['mixed model', 'modèle mixte', 'multilevel']
        }

        methods = []
        text_lower = text.lower()

        for method_name, keywords in statistical_tests.items():
            if any(keyword in text_lower for keyword in keywords):
                methods.append({
                    'method': method_name,
                    'mentioned': True
                })

        return methods

    def _analyze_experimental_design(self, text: str, methodology_section: Optional[Dict]) -> Dict:
        """Analyse le design expérimental."""
        search_text = (methodology_section['content'] if methodology_section else text).lower()

        design_features = {
            'randomized': 'randomis' in search_text or 'random' in search_text,
            'controlled': 'contrôl' in search_text or 'control' in search_text,
            'blinded': 'aveugle' in search_text or 'blind' in search_text,
            'double_blind': 'double aveugle' in search_text or 'double-blind' in search_text,
            'placebo': 'placebo' in search_text,
            'crossover': 'cross-over' in search_text or 'croisé' in search_text,
            'longitudinal': 'longitudinal' in search_text,
            'repeated_measures': 'mesures répétées' in search_text or 'repeated measures' in search_text
        }

        # Déterminer le type de design
        if design_features['randomized'] and design_features['controlled']:
            design_type = 'Essai contrôlé randomisé (RCT)'
        elif design_features['randomized']:
            design_type = 'Randomisé'
        elif design_features['controlled']:
            design_type = 'Contrôlé'
        else:
            design_type = 'Non spécifié'

        return {
            'design_type': design_type,
            'features': {k: v for k, v in design_features.items() if v}
        }

    def _extract_data_collection_info(self, text: str, methodology_section: Optional[Dict]) -> Dict:
        """Extrait les informations sur la collecte de données."""
        search_text = methodology_section['content'] if methodology_section else text

        collection_info = {
            'methods': [],
            'duration': None,
            'frequency': None,
            'instruments': []
        }

        # Méthodes de collecte
        collection_methods = {
            'Questionnaire': ['questionnaire', 'survey'],
            'Entretien': ['entretien', 'interview'],
            'Observation': ['observation'],
            'Mesure': ['mesure', 'measurement'],
            'Capteur': ['capteur', 'sensor'],
            'Enregistrement': ['enregistrement', 'recording'],
            'Base de données': ['database', 'base de données']
        }

        text_lower = search_text.lower()

        for method, keywords in collection_methods.items():
            if any(keyword in text_lower for keyword in keywords):
                collection_info['methods'].append(method)

        # Durée
        duration_match = re.search(r'(?:pendant|during|over)\s+(\d+)\s+(jour|day|semaine|week|mois|month|année|year)', search_text, re.IGNORECASE)
        if duration_match:
            collection_info['duration'] = f"{duration_match.group(1)} {duration_match.group(2)}"

        return collection_info

    def _extract_sample_info(self, text: str) -> Dict:
        """Extrait les informations sur l'échantillon."""
        sample_info = {
            'size': None,
            'description': None,
            'criteria': []
        }

        # Taille de l'échantillon
        size_patterns = [
            r'[Nn]\s*=\s*(\d+)',
            r'(\d+)\s+(?:participants|subjects|sujets|patients)',
            r'échantillon de\s+(\d+)',
            r'sample (?:of|size)\s+(\d+)'
        ]

        for pattern in size_patterns:
            match = re.search(pattern, text)
            if match:
                sample_info['size'] = int(match.group(1))
                break

        # Critères d'inclusion/exclusion
        if 'critères d\'inclusion' in text.lower() or 'inclusion criteria' in text.lower():
            sample_info['criteria'].append('Critères d\'inclusion définis')

        if 'critères d\'exclusion' in text.lower() or 'exclusion criteria' in text.lower():
            sample_info['criteria'].append('Critères d\'exclusion définis')

        return sample_info

    def _extract_protocol_steps(self, methodology_section: Optional[Dict]) -> List[Dict]:
        """Extrait les étapes du protocole."""
        if not methodology_section:
            return []

        content = methodology_section['content']
        steps = []

        # Rechercher des listes numérotées ou à puces
        lines = content.split('\n')

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Étapes numérotées
            step_match = re.match(r'^(\d+)[\.\)]\s+(.+)', line_stripped)
            if step_match:
                steps.append({
                    'number': int(step_match.group(1)),
                    'description': step_match.group(2),
                    'type': 'numbered'
                })

            # Étapes avec mots-clés
            elif any(keyword in line_stripped.lower() for keyword in ['étape', 'step', 'phase', 'first', 'second', 'then', 'finally']):
                steps.append({
                    'number': len(steps) + 1,
                    'description': line_stripped,
                    'type': 'keyword'
                })

        return steps[:20]  # Limiter à 20 étapes

    def _assess_validity(self, text: str) -> Dict:
        """Évalue les indicateurs de validité méthodologique."""
        text_lower = text.lower()

        validity_indicators = {
            'internal_validity': any(term in text_lower for term in [
                'validité interne', 'internal validity', 'contrôle des variables'
            ]),
            'external_validity': any(term in text_lower for term in [
                'validité externe', 'external validity', 'généralisabilité', 'generalizability'
            ]),
            'construct_validity': any(term in text_lower for term in [
                'validité de construit', 'construct validity'
            ]),
            'reliability': any(term in text_lower for term in [
                'fiabilité', 'reliability', 'reproductibilité', 'reproducibility',
                'cohérence', 'consistency', 'alpha de cronbach', 'cronbach'
            ]),
            'peer_review': 'peer review' in text_lower or 'revue par les pairs' in text_lower,
            'ethics_approval': any(term in text_lower for term in [
                'comité d\'éthique', 'ethics committee', 'irb', 'approbation éthique'
            ])
        }

        return validity_indicators

    def _calculate_rigor_score(self, analysis: Dict) -> float:
        """
        Calcule un score de rigueur méthodologique (0-100).

        Basé sur :
        - Présence d'une section méthodologie claire
        - Type d'approche bien défini
        - Méthodes statistiques appropriées
        - Design expérimental robuste
        - Informations sur l'échantillon
        - Indicateurs de validité
        """
        score = 0.0

        # Section méthodologie (20 points)
        if analysis['methodology_section']:
            score += 20

        # Type d'approche (15 points)
        if analysis['approach_type']['main_type'] != 'Approche non spécifiée':
            score += 15

        # Méthodes statistiques (15 points)
        if len(analysis['statistical_methods']) > 0:
            score += min(15, len(analysis['statistical_methods']) * 3)

        # Design expérimental (20 points)
        design_features = analysis['experimental_design'].get('features', {})
        score += len(design_features) * 5

        # Informations échantillon (15 points)
        if analysis['sample_info']['size']:
            score += 10
        if analysis['sample_info']['criteria']:
            score += 5

        # Indicateurs de validité (15 points)
        validity_count = sum(1 for v in analysis['validity_indicators'].values() if v)
        score += validity_count * 2.5

        return min(100.0, round(score, 1))

    def _classify_method(self, method_name: str) -> str:
        """Classifie une méthode."""
        method_lower = method_name.lower()

        if any(term in method_lower for term in ['statistique', 'statistical', 'régression', 'anova']):
            return 'Statistique'
        elif any(term in method_lower for term in ['qualitatif', 'qualitative', 'entretien', 'ethnograph']):
            return 'Qualitative'
        elif any(term in method_lower for term in ['expérimental', 'experimental', 'essai', 'trial']):
            return 'Expérimentale'
        elif any(term in method_lower for term in ['computationnel', 'computational', 'simulation', 'modélisation']):
            return 'Computationnelle'
        else:
            return 'Autre'

    def _classify_tool(self, tool_name: str) -> str:
        """Classifie un outil."""
        tool_lower = tool_name.lower()

        if any(lang in tool_lower for lang in ['python', 'r ', 'matlab', 'julia']):
            return 'Langage de programmation'
        elif any(soft in tool_lower for soft in ['spss', 'stata', 'sas', 'excel']):
            return 'Logiciel statistique'
        elif any(soft in tool_lower for lang in ['tensorflow', 'pytorch', 'scikit']):
            return 'Machine Learning'
        else:
            return 'Outil général'
