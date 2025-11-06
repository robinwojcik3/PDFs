"""
Service de détection et extraction d'équations mathématiques.
"""
import re
from typing import List, Dict, Optional

class EquationDetector:
    """Détecteur d'équations mathématiques dans les documents."""

    def __init__(self):
        # Symboles mathématiques courants
        self.math_symbols = [
            '∑', '∫', '∂', '∇', '√', '∞', '≈', '≠', '≤', '≥',
            '±', '×', '÷', '∈', '∉', '⊂', '⊃', '∪', '∩',
            'α', 'β', 'γ', 'δ', 'ε', 'θ', 'λ', 'μ', 'π', 'σ', 'τ', 'φ', 'ω',
            'Δ', 'Σ', 'Π', 'Ω'
        ]

        # Patterns pour détecter les équations
        self.equation_patterns = [
            r'[a-zA-Z]\s*=\s*[^=\n]{5,}',  # Variable = expression
            r'\b\w+\s*[+\-*/]\s*\w+\s*=\s*\w+',  # Opérations mathématiques
            r'\([^)]{10,}\)\s*=\s*[^=\n]+',  # (expression) = ...
            r'\$\$.*?\$\$',  # LaTeX display mode
            r'\$.*?\$',  # LaTeX inline mode
            r'\\begin{equation}.*?\\end{equation}',  # LaTeX equation
            r'\\begin{align}.*?\\end{align}',  # LaTeX align
        ]

    def detect_equations(self, text: str) -> List[Dict[str, any]]:
        """
        Détecte toutes les équations dans le texte.

        Args:
            text: Texte du document

        Returns:
            Liste d'équations détectées
        """
        equations = []
        equation_id = 0

        # Détecter par patterns
        for pattern in self.equation_patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.MULTILINE)

            for match in matches:
                equation_text = match.group(0)

                # Vérifier que c'est vraiment une équation
                if self._is_likely_equation(equation_text):
                    equation_id += 1
                    equations.append({
                        'id': f'eq_{equation_id}',
                        'content': equation_text.strip(),
                        'position': match.start(),
                        'type': self._detect_equation_type(equation_text),
                        'latex': self._extract_latex(equation_text),
                        'variables': self._extract_variables(equation_text),
                        'operators': self._extract_operators(equation_text)
                    })

        # Détecter par présence de symboles mathématiques
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if self._contains_math_symbols(line) and len(line.strip()) > 5:
                # Vérifier si déjà détectée
                if not any(eq['content'] in line for eq in equations):
                    equation_id += 1
                    equations.append({
                        'id': f'eq_{equation_id}',
                        'content': line.strip(),
                        'position': text.find(line),
                        'type': 'symbolic',
                        'latex': None,
                        'variables': self._extract_variables(line),
                        'operators': self._extract_operators(line)
                    })

        return sorted(equations, key=lambda x: x['position'])

    def _is_likely_equation(self, text: str) -> bool:
        """Détermine si un texte est probablement une équation."""
        # Critères :
        # - Contient au moins un symbole mathématique ou opérateur
        # - Contient un signe égal
        # - Pas trop long (< 500 caractères)
        # - Pas une phrase complète (peu de mots communs)

        if len(text) > 500:
            return False

        has_equals = '=' in text
        has_math_symbols = self._contains_math_symbols(text)
        has_operators = any(op in text for op in ['+', '-', '*', '/', '^'])

        # Compter les mots communs français/anglais
        common_words = ['le', 'la', 'les', 'un', 'une', 'de', 'the', 'a', 'an', 'is', 'are', 'was', 'were']
        word_count = sum(1 for word in common_words if f' {word} ' in text.lower())

        return (has_equals or has_math_symbols or has_operators) and word_count < 3

    def _contains_math_symbols(self, text: str) -> bool:
        """Vérifie si le texte contient des symboles mathématiques."""
        return any(symbol in text for symbol in self.math_symbols)

    def _detect_equation_type(self, equation: str) -> str:
        """Détecte le type d'équation."""
        if '$$' in equation or '\\begin{equation}' in equation:
            return 'latex_display'
        elif '$' in equation:
            return 'latex_inline'
        elif any(symbol in equation for symbol in self.math_symbols):
            return 'symbolic'
        elif re.search(r'[a-zA-Z]\s*=', equation):
            return 'algebraic'
        else:
            return 'arithmetic'

    def _extract_latex(self, equation: str) -> Optional[str]:
        """Extrait le code LaTeX si présent."""
        # LaTeX display mode
        match = re.search(r'\$\$(.*?)\$\$', equation, re.DOTALL)
        if match:
            return match.group(1).strip()

        # LaTeX inline mode
        match = re.search(r'\$(.*?)\$', equation)
        if match:
            return match.group(1).strip()

        # LaTeX environment
        match = re.search(r'\\begin{(?:equation|align)}(.*?)\\end{(?:equation|align)}', equation, re.DOTALL)
        if match:
            return match.group(1).strip()

        return None

    def _extract_variables(self, equation: str) -> List[str]:
        """Extrait les variables de l'équation."""
        # Extraire les lettres isolées ou avec indices
        variables = re.findall(r'\b[a-zA-Z](?:_[a-zA-Z0-9]+)?\b', equation)

        # Filtrer les mots courants
        excluded = {'e', 'i', 'a', 'o', 'x', 'y', 'z', 't', 'n', 'k'}  # Garder x, y, z qui sont souvent des variables

        variables = [v for v in variables if len(v) <= 3]

        return list(set(variables))

    def _extract_operators(self, equation: str) -> List[str]:
        """Extrait les opérateurs de l'équation."""
        operators = []

        # Opérateurs de base
        for op in ['+', '-', '*', '/', '^', '=', '<', '>', '≈', '≠', '≤', '≥']:
            if op in equation:
                operators.append(op)

        # Opérateurs spéciaux
        for op in ['∑', '∫', '∂', '∇', '√']:
            if op in equation:
                operators.append(op)

        return operators

    def convert_to_latex(self, equation: str) -> str:
        """
        Convertit une équation en format LaTeX (basique).

        Args:
            equation: Équation en texte brut

        Returns:
            Équation en LaTeX
        """
        # Si déjà en LaTeX, retourner tel quel
        if '$' in equation or '\\' in equation:
            return equation

        latex = equation

        # Remplacer les symboles
        replacements = {
            '>=': '\\geq',
            '<=': '\\leq',
            '!=': '\\neq',
            '~=': '\\approx',
            'sqrt': '\\sqrt',
            'sum': '\\sum',
            'int': '\\int',
            'alpha': '\\alpha',
            'beta': '\\beta',
            'gamma': '\\gamma',
            'delta': '\\delta',
            'epsilon': '\\epsilon',
            'theta': '\\theta',
            'lambda': '\\lambda',
            'mu': '\\mu',
            'pi': '\\pi',
            'sigma': '\\sigma',
            'tau': '\\tau',
            'phi': '\\phi',
            'omega': '\\omega',
        }

        for old, new in replacements.items():
            latex = latex.replace(old, new)

        # Mettre les indices en format LaTeX
        latex = re.sub(r'(\w)_(\w+)', r'\1_{\2}', latex)

        # Mettre les exposants en format LaTeX
        latex = re.sub(r'(\w)\^(\w+)', r'\1^{\2}', latex)

        return f'${latex}$'

    def get_equation_statistics(self, equations: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Calcule des statistiques sur les équations.

        Args:
            equations: Liste d'équations

        Returns:
            Statistiques
        """
        stats = {
            'total_equations': len(equations),
            'by_type': {},
            'common_variables': {},
            'common_operators': {},
            'with_latex': 0,
            'average_length': 0
        }

        if not equations:
            return stats

        # Compter par type
        for eq in equations:
            eq_type = eq['type']
            stats['by_type'][eq_type] = stats['by_type'].get(eq_type, 0) + 1

            if eq['latex']:
                stats['with_latex'] += 1

            # Compter variables
            for var in eq['variables']:
                stats['common_variables'][var] = stats['common_variables'].get(var, 0) + 1

            # Compter opérateurs
            for op in eq['operators']:
                stats['common_operators'][op] = stats['common_operators'].get(op, 0) + 1

        # Trier par fréquence
        stats['common_variables'] = dict(sorted(
            stats['common_variables'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10])

        stats['common_operators'] = dict(sorted(
            stats['common_operators'].items(),
            key=lambda x: x[1],
            reverse=True
        ))

        # Longueur moyenne
        total_length = sum(len(eq['content']) for eq in equations)
        stats['average_length'] = total_length / len(equations)

        return stats
