"""
Service de comparaison de documents PDF.
"""
from typing import List, Dict, Set
from difflib import SequenceMatcher
from collections import Counter
import re

class DocumentComparator:
    """Comparateur de documents scientifiques."""

    def compare_documents(self, doc1: Dict, doc2: Dict) -> Dict:
        """
        Compare deux documents de manière complète.

        Args:
            doc1: Premier document
            doc2: Second document

        Returns:
            Rapport de comparaison détaillé
        """
        comparison = {
            'metadata_comparison': self._compare_metadata(doc1, doc2),
            'content_similarity': self._compare_content(doc1, doc2),
            'structure_comparison': self._compare_structure(doc1, doc2),
            'keywords_overlap': self._compare_keywords(doc1, doc2),
            'authors_overlap': self._compare_authors(doc1, doc2),
            'visual_elements': self._compare_visual_elements(doc1, doc2),
            'overall_similarity_score': 0.0
        }

        # Calculer le score global de similarité
        comparison['overall_similarity_score'] = self._calculate_overall_similarity(comparison)

        return comparison

    def compare_multiple(self, documents: List[Dict]) -> Dict:
        """
        Compare plusieurs documents entre eux.

        Args:
            documents: Liste de documents à comparer

        Returns:
            Matrice de similarité et analyses
        """
        n = len(documents)
        similarity_matrix = [[0.0 for _ in range(n)] for _ in range(n)]

        # Calculer les similarités par paires
        for i in range(n):
            for j in range(i + 1, n):
                comparison = self.compare_documents(documents[i], documents[j])
                score = comparison['overall_similarity_score']
                similarity_matrix[i][j] = score
                similarity_matrix[j][i] = score

        # Identifier les clusters de documents similaires
        clusters = self._identify_clusters(similarity_matrix, documents, threshold=0.6)

        return {
            'similarity_matrix': similarity_matrix,
            'documents': [{'id': doc['id'], 'title': doc.get('metadata', {}).get('title', doc['filename'])} for doc in documents],
            'clusters': clusters,
            'most_similar_pairs': self._find_most_similar_pairs(similarity_matrix, documents),
            'most_different_pairs': self._find_most_different_pairs(similarity_matrix, documents)
        }

    def _compare_metadata(self, doc1: Dict, doc2: Dict) -> Dict:
        """Compare les métadonnées de deux documents."""
        meta1 = doc1.get('metadata', {})
        meta2 = doc2.get('metadata', {})

        comparison = {
            'same_authors': False,
            'common_authors': [],
            'year_difference': None,
            'same_keywords': False,
            'common_keywords': []
        }

        # Comparer les auteurs
        authors1 = set(meta1.get('authors', []))
        authors2 = set(meta2.get('authors', []))

        if authors1 and authors2:
            comparison['common_authors'] = list(authors1.intersection(authors2))
            comparison['same_authors'] = authors1 == authors2

        # Comparer les années
        year1 = meta1.get('year')
        year2 = meta2.get('year')

        if year1 and year2:
            comparison['year_difference'] = abs(year1 - year2)

        # Comparer les mots-clés
        keywords1 = set(meta1.get('keywords', []))
        keywords2 = set(meta2.get('keywords', []))

        if keywords1 and keywords2:
            comparison['common_keywords'] = list(keywords1.intersection(keywords2))
            comparison['same_keywords'] = keywords1 == keywords2

        return comparison

    def _compare_content(self, doc1: Dict, doc2: Dict) -> Dict:
        """Compare le contenu textuel de deux documents."""
        text1 = doc1.get('full_text', '')
        text2 = doc2.get('full_text', '')

        # Similarité de séquence
        sequence_similarity = SequenceMatcher(None, text1, text2).ratio()

        # Similarité basée sur les mots
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))

        if words1 and words2:
            word_similarity = len(words1.intersection(words2)) / len(words1.union(words2))
        else:
            word_similarity = 0.0

        # Phrases communes (extraits de 5+ mots)
        common_phrases = self._find_common_phrases(text1, text2)

        return {
            'sequence_similarity': round(sequence_similarity, 3),
            'word_similarity': round(word_similarity, 3),
            'common_words_count': len(words1.intersection(words2)),
            'unique_to_doc1': len(words1 - words2),
            'unique_to_doc2': len(words2 - words1),
            'common_phrases': common_phrases[:10]  # Top 10
        }

    def _compare_structure(self, doc1: Dict, doc2: Dict) -> Dict:
        """Compare la structure des documents."""
        sections1 = doc1.get('sections', [])
        sections2 = doc2.get('sections', [])

        # Titres de sections
        titles1 = [s['title'].lower() for s in sections1]
        titles2 = [s['title'].lower() for s in sections2]

        common_section_titles = list(set(titles1).intersection(set(titles2)))

        return {
            'sections_count_doc1': len(sections1),
            'sections_count_doc2': len(sections2),
            'common_section_titles': common_section_titles,
            'structure_similarity': len(common_section_titles) / max(len(titles1), len(titles2)) if max(len(titles1), len(titles2)) > 0 else 0
        }

    def _compare_keywords(self, doc1: Dict, doc2: Dict) -> Dict:
        """Compare les mots-clés et concepts."""
        meta1 = doc1.get('metadata', {})
        meta2 = doc2.get('metadata', {})

        keywords1 = set(k.lower() for k in meta1.get('keywords', []))
        keywords2 = set(k.lower() for k in meta2.get('keywords', []))

        if not keywords1 or not keywords2:
            return {
                'overlap_count': 0,
                'overlap_ratio': 0.0,
                'common_keywords': []
            }

        common = keywords1.intersection(keywords2)

        return {
            'overlap_count': len(common),
            'overlap_ratio': len(common) / len(keywords1.union(keywords2)),
            'common_keywords': list(common)
        }

    def _compare_authors(self, doc1: Dict, doc2: Dict) -> Dict:
        """Compare les auteurs."""
        meta1 = doc1.get('metadata', {})
        meta2 = doc2.get('metadata', {})

        authors1 = set(a.lower() for a in meta1.get('authors', []))
        authors2 = set(a.lower() for a in meta2.get('authors', []))

        if not authors1 or not authors2:
            return {
                'overlap_count': 0,
                'overlap_ratio': 0.0,
                'common_authors': []
            }

        common = authors1.intersection(authors2)

        return {
            'overlap_count': len(common),
            'overlap_ratio': len(common) / len(authors1.union(authors2)),
            'common_authors': list(common)
        }

    def _compare_visual_elements(self, doc1: Dict, doc2: Dict) -> Dict:
        """Compare les éléments visuels (figures, tableaux)."""
        return {
            'figures_doc1': len(doc1.get('figures', [])),
            'figures_doc2': len(doc2.get('figures', [])),
            'tables_doc1': len(doc1.get('tables', [])),
            'tables_doc2': len(doc2.get('tables', [])),
            'visual_density_doc1': (len(doc1.get('figures', [])) + len(doc1.get('tables', []))) / doc1.get('num_pages', 1),
            'visual_density_doc2': (len(doc2.get('figures', [])) + len(doc2.get('tables', []))) / doc2.get('num_pages', 1)
        }

    def _find_common_phrases(self, text1: str, text2: str, min_length: int = 5) -> List[str]:
        """Trouve les phrases communes entre deux textes."""
        # Diviser en phrases (approximation simple)
        sentences1 = re.split(r'[.!?]+', text1)
        sentences2 = re.split(r'[.!?]+', text2)

        common_phrases = []

        for s1 in sentences1:
            s1_clean = ' '.join(s1.split()).lower()
            if len(s1_clean.split()) < min_length:
                continue

            for s2 in sentences2:
                s2_clean = ' '.join(s2.split()).lower()

                # Vérifier la similarité
                similarity = SequenceMatcher(None, s1_clean, s2_clean).ratio()

                if similarity > 0.8:  # 80% de similarité
                    common_phrases.append(s1.strip())
                    break

        return common_phrases

    def _calculate_overall_similarity(self, comparison: Dict) -> float:
        """Calcule un score global de similarité."""
        scores = []

        # Contenu (poids: 40%)
        content_sim = comparison['content_similarity']
        scores.append(content_sim.get('word_similarity', 0) * 0.4)

        # Structure (poids: 20%)
        struct_sim = comparison['structure_comparison']
        scores.append(struct_sim.get('structure_similarity', 0) * 0.2)

        # Mots-clés (poids: 20%)
        keywords_sim = comparison['keywords_overlap']
        scores.append(keywords_sim.get('overlap_ratio', 0) * 0.2)

        # Auteurs (poids: 20%)
        authors_sim = comparison['authors_overlap']
        scores.append(authors_sim.get('overlap_ratio', 0) * 0.2)

        return round(sum(scores), 3)

    def _identify_clusters(self, similarity_matrix: List[List[float]], documents: List[Dict], threshold: float = 0.6) -> List[Dict]:
        """Identifie les clusters de documents similaires."""
        n = len(documents)
        clusters = []
        assigned = set()

        for i in range(n):
            if i in assigned:
                continue

            cluster = [i]
            assigned.add(i)

            for j in range(i + 1, n):
                if j not in assigned and similarity_matrix[i][j] >= threshold:
                    cluster.append(j)
                    assigned.add(j)

            if len(cluster) > 1:
                clusters.append({
                    'documents': [
                        {
                            'id': documents[idx]['id'],
                            'title': documents[idx].get('metadata', {}).get('title', documents[idx]['filename'])
                        }
                        for idx in cluster
                    ],
                    'size': len(cluster),
                    'average_similarity': sum(similarity_matrix[i][j] for i in cluster for j in cluster if i < j) / (len(cluster) * (len(cluster) - 1) / 2) if len(cluster) > 1 else 0
                })

        return clusters

    def _find_most_similar_pairs(self, similarity_matrix: List[List[float]], documents: List[Dict], top_n: int = 5) -> List[Dict]:
        """Trouve les paires de documents les plus similaires."""
        pairs = []

        for i in range(len(documents)):
            for j in range(i + 1, len(documents)):
                pairs.append({
                    'doc1': {
                        'id': documents[i]['id'],
                        'title': documents[i].get('metadata', {}).get('title', documents[i]['filename'])
                    },
                    'doc2': {
                        'id': documents[j]['id'],
                        'title': documents[j].get('metadata', {}).get('title', documents[j]['filename'])
                    },
                    'similarity': similarity_matrix[i][j]
                })

        pairs.sort(key=lambda x: x['similarity'], reverse=True)
        return pairs[:top_n]

    def _find_most_different_pairs(self, similarity_matrix: List[List[float]], documents: List[Dict], top_n: int = 5) -> List[Dict]:
        """Trouve les paires de documents les plus différentes."""
        pairs = []

        for i in range(len(documents)):
            for j in range(i + 1, len(documents)):
                pairs.append({
                    'doc1': {
                        'id': documents[i]['id'],
                        'title': documents[i].get('metadata', {}).get('title', documents[i]['filename'])
                    },
                    'doc2': {
                        'id': documents[j]['id'],
                        'title': documents[j].get('metadata', {}).get('title', documents[j]['filename'])
                    },
                    'similarity': similarity_matrix[i][j]
                })

        pairs.sort(key=lambda x: x['similarity'])
        return pairs[:top_n]
