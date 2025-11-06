"""
Service d'extraction de références bibliographiques.
"""
import re
from typing import List, Dict, Optional
from collections import defaultdict

class BibliographyExtractor:
    """Extracteur de références bibliographiques des PDFs."""

    def __init__(self):
        # Patterns pour détecter les citations
        self.citation_patterns = [
            r'\[(\d+)\]',  # [1], [2], etc.
            r'\[(\d+[-,]\d+)\]',  # [1-3], [1,2], etc.
            r'\(([A-Z][a-z]+(?:\s+(?:et\s+al\.|and|&)\s+[A-Z][a-z]+)?,?\s+\d{4}[a-z]?)\)',  # (Author, 2020)
            r'([A-Z][a-z]+\s+et\s+al\.\s+\(\d{4}\))',  # Author et al. (2020)
        ]

        # Patterns pour la section bibliographie
        self.biblio_section_patterns = [
            r'(?:références|references|bibliographie|bibliography)\s*$',
            r'^\s*\d+\.\s+[A-Z]',  # Commence par un numéro
            r'^\[[^\]]+\]\s+[A-Z]',  # Commence par [auteur]
        ]

    def extract_citations(self, text: str) -> List[Dict[str, any]]:
        """
        Extrait toutes les citations du texte.

        Args:
            text: Texte du document

        Returns:
            Liste des citations trouvées
        """
        citations = []
        seen = set()

        for pattern in self.citation_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)

            for match in matches:
                citation_text = match.group(0)
                citation_ref = match.group(1)

                if citation_text not in seen:
                    seen.add(citation_text)
                    citations.append({
                        'text': citation_text,
                        'reference': citation_ref,
                        'position': match.start(),
                        'type': self._detect_citation_type(citation_text)
                    })

        return sorted(citations, key=lambda x: x['position'])

    def extract_bibliography(self, text: str) -> List[Dict[str, str]]:
        """
        Extrait la section bibliographie complète.

        Args:
            text: Texte complet du document

        Returns:
            Liste des références bibliographiques
        """
        # Trouver la section bibliographie
        biblio_start = self._find_bibliography_section(text)

        if biblio_start == -1:
            return []

        biblio_text = text[biblio_start:]

        # Extraire les références individuelles
        references = self._parse_bibliography(biblio_text)

        return references

    def _find_bibliography_section(self, text: str) -> int:
        """Trouve le début de la section bibliographie."""
        lines = text.split('\n')

        for i, line in enumerate(lines):
            line_clean = line.strip().lower()

            # Chercher les titres de section
            if any(re.search(pattern, line_clean, re.IGNORECASE) for pattern in self.biblio_section_patterns[:1]):
                # Retourner la position dans le texte original
                return text.find(line)

        # Si pas trouvé, chercher dans les dernières 20% du document
        start_pos = int(len(text) * 0.8)
        return start_pos

    def _parse_bibliography(self, biblio_text: str) -> List[Dict[str, str]]:
        """Parse les références de la bibliographie."""
        references = []
        lines = biblio_text.split('\n')

        current_ref = []
        ref_number = 0

        for line in lines:
            line = line.strip()

            # Vérifier si c'est le début d'une nouvelle référence
            if re.match(r'^\[?\d+\]?\s+', line) or re.match(r'^\[[^\]]+\]', line):
                # Sauvegarder la référence précédente
                if current_ref:
                    ref_number += 1
                    references.append(self._parse_reference(' '.join(current_ref), ref_number))

                # Commencer une nouvelle référence
                current_ref = [line]
            elif line and current_ref:
                # Continuer la référence actuelle
                current_ref.append(line)

        # Ajouter la dernière référence
        if current_ref:
            ref_number += 1
            references.append(self._parse_reference(' '.join(current_ref), ref_number))

        return references

    def _parse_reference(self, ref_text: str, number: int) -> Dict[str, str]:
        """Parse une référence individuelle."""
        ref_data = {
            'number': number,
            'raw': ref_text,
            'authors': None,
            'year': None,
            'title': None,
            'journal': None,
            'doi': None,
            'url': None
        }

        # Extraire l'année
        year_match = re.search(r'\b(19|20)\d{2}\b', ref_text)
        if year_match:
            ref_data['year'] = int(year_match.group(0))

        # Extraire le DOI
        doi_match = re.search(r'(?:doi|DOI):\s*(10\.\d+/[^\s]+)', ref_text)
        if doi_match:
            ref_data['doi'] = doi_match.group(1)

        # Extraire l'URL
        url_match = re.search(r'https?://[^\s]+', ref_text)
        if url_match:
            ref_data['url'] = url_match.group(0)

        # Extraire les auteurs (première partie avant l'année généralement)
        if ref_data['year']:
            authors_text = ref_text.split(str(ref_data['year']))[0]
            ref_data['authors'] = authors_text.strip(' .,[]()0123456789')

        # Extraire le titre (entre guillemets ou après auteurs)
        title_match = re.search(r'["\'](.*?)["\']', ref_text)
        if title_match:
            ref_data['title'] = title_match.group(1)

        return ref_data

    def _detect_citation_type(self, citation: str) -> str:
        """Détecte le type de citation."""
        if re.match(r'\[\d+\]', citation):
            return 'numeric'
        elif re.match(r'\([A-Z]', citation):
            return 'author-year'
        else:
            return 'other'

    def format_reference(self, ref: Dict[str, str], style: str = 'apa') -> str:
        """
        Formate une référence selon un style donné.

        Args:
            ref: Dictionnaire de référence
            style: Style de citation (apa, ieee, chicago)

        Returns:
            Référence formatée
        """
        if style == 'apa':
            return self._format_apa(ref)
        elif style == 'ieee':
            return self._format_ieee(ref)
        elif style == 'chicago':
            return self._format_chicago(ref)
        else:
            return ref['raw']

    def _format_apa(self, ref: Dict[str, str]) -> str:
        """Format APA."""
        parts = []

        if ref['authors']:
            parts.append(f"{ref['authors']}")

        if ref['year']:
            parts.append(f"({ref['year']})")

        if ref['title']:
            parts.append(f"{ref['title']}.")

        if ref['journal']:
            parts.append(f"{ref['journal']}.")

        if ref['doi']:
            parts.append(f"https://doi.org/{ref['doi']}")

        return ' '.join(parts) if parts else ref['raw']

    def _format_ieee(self, ref: Dict[str, str]) -> str:
        """Format IEEE."""
        parts = []

        if ref['authors']:
            parts.append(f"{ref['authors']},")

        if ref['title']:
            parts.append(f'"{ref["title"]},"')

        if ref['journal']:
            parts.append(f"{ref['journal']},")

        if ref['year']:
            parts.append(f"{ref['year']}.")

        return ' '.join(parts) if parts else ref['raw']

    def _format_chicago(self, ref: Dict[str, str]) -> str:
        """Format Chicago."""
        parts = []

        if ref['authors']:
            parts.append(f"{ref['authors']}.")

        if ref['title']:
            parts.append(f'"{ref["title"]}."')

        if ref['journal']:
            parts.append(f"{ref['journal']}")

        if ref['year']:
            parts.append(f"({ref['year']}).")

        return ' '.join(parts) if parts else ref['raw']

    def export_to_bibtex(self, references: List[Dict[str, str]]) -> str:
        """
        Exporte les références en format BibTeX.

        Args:
            references: Liste de références

        Returns:
            String BibTeX
        """
        bibtex_entries = []

        for ref in references:
            entry_id = f"ref{ref['number']}"

            entry = f"@article{{{entry_id},\n"

            if ref['authors']:
                entry += f"  author = {{{ref['authors']}}},\n"

            if ref['title']:
                entry += f"  title = {{{ref['title']}}},\n"

            if ref['journal']:
                entry += f"  journal = {{{ref['journal']}}},\n"

            if ref['year']:
                entry += f"  year = {{{ref['year']}}},\n"

            if ref['doi']:
                entry += f"  doi = {{{ref['doi']}}},\n"

            entry += "}\n"
            bibtex_entries.append(entry)

        return '\n'.join(bibtex_entries)

    def get_citation_statistics(self, citations: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Calcule des statistiques sur les citations.

        Args:
            citations: Liste de citations

        Returns:
            Statistiques
        """
        stats = {
            'total_citations': len(citations),
            'citation_types': defaultdict(int),
            'most_cited': defaultdict(int)
        }

        for citation in citations:
            stats['citation_types'][citation['type']] += 1

            # Compter les références les plus citées
            ref = citation['reference']
            stats['most_cited'][ref] += 1

        # Trier les plus citées
        stats['most_cited'] = dict(sorted(
            stats['most_cited'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10])

        return stats
