"""
Système de recommandation de documents.
"""
from typing import List, Dict, Optional
from collections import Counter
import re

class DocumentRecommender:
    """Moteur de recommandation de documents."""

    def __init__(self, documents_cache: Dict):
        """
        Initialise le recommandeur.

        Args:
            documents_cache: Cache des documents indexés
        """
        self.documents = documents_cache

    def recommend_similar(
        self,
        document_id: str,
        limit: int = 5,
        min_score: float = 0.3
    ) -> List[Dict]:
        """
        Recommande des documents similaires.

        Args:
            document_id: ID du document source
            limit: Nombre de recommandations
            min_score: Score minimum de similarité

        Returns:
            Liste de recommandations avec scores
        """
        if document_id not in self.documents:
            return []

        source_doc = self.documents[document_id]
        recommendations = []

        for doc_id, doc in self.documents.items():
            if doc_id == document_id:
                continue

            score = self._calculate_similarity(source_doc, doc)

            if score >= min_score:
                recommendations.append({
                    'document_id': doc_id,
                    'title': doc.get('metadata', {}).get('title', doc['filename']),
                    'authors': doc.get('metadata', {}).get('authors', []),
                    'year': doc.get('metadata', {}).get('year'),
                    'similarity_score': round(score, 3),
                    'reasons': self._explain_similarity(source_doc, doc)
                })

        # Trier par score de similarité
        recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)

        return recommendations[:limit]

    def recommend_by_reading_history(
        self,
        reading_history: List[Dict],
        limit: int = 5
    ) -> List[Dict]:
        """
        Recommande basé sur l'historique de lecture.

        Args:
            reading_history: Historique de lecture de l'utilisateur
            limit: Nombre de recommandations

        Returns:
            Liste de recommandations
        """
        if not reading_history:
            return self._recommend_popular(limit)

        # Extraire les documents les plus lus
        most_read_ids = [
            h['document_id'] for h in
            sorted(reading_history, key=lambda x: x.get('total_views', 0), reverse=True)[:5]
        ]

        # Trouver des documents similaires aux plus lus
        all_recommendations = {}

        for doc_id in most_read_ids:
            if doc_id in self.documents:
                similar = self.recommend_similar(doc_id, limit=limit)

                for rec in similar:
                    rec_id = rec['document_id']

                    # Éviter de recommander des documents déjà lus
                    if rec_id not in most_read_ids:
                        if rec_id not in all_recommendations:
                            all_recommendations[rec_id] = rec
                        else:
                            # Augmenter le score si recommandé plusieurs fois
                            all_recommendations[rec_id]['similarity_score'] += rec['similarity_score'] * 0.5

        # Trier et limiter
        recommendations = sorted(
            all_recommendations.values(),
            key=lambda x: x['similarity_score'],
            reverse=True
        )

        return recommendations[:limit]

    def recommend_by_topic(
        self,
        keywords: List[str],
        limit: int = 5
    ) -> List[Dict]:
        """
        Recommande des documents par thématique.

        Args:
            keywords: Mots-clés de recherche
            limit: Nombre de recommandations

        Returns:
            Liste de recommandations
        """
        recommendations = []
        keywords_lower = [k.lower() for k in keywords]

        for doc_id, doc in self.documents.items():
            score = 0

            # Chercher dans les mots-clés du document
            doc_keywords = [k.lower() for k in doc.get('metadata', {}).get('keywords', [])]
            matching_keywords = set(keywords_lower).intersection(set(doc_keywords))
            score += len(matching_keywords) * 2

            # Chercher dans le titre
            title = doc.get('metadata', {}).get('title', '').lower()
            for keyword in keywords_lower:
                if keyword in title:
                    score += 1.5

            # Chercher dans le texte complet
            full_text = doc.get('full_text', '').lower()
            for keyword in keywords_lower:
                # Compter les occurrences (limitées pour éviter les biais)
                occurrences = min(full_text.count(keyword), 10)
                score += occurrences * 0.1

            if score > 0:
                recommendations.append({
                    'document_id': doc_id,
                    'title': doc.get('metadata', {}).get('title', doc['filename']),
                    'authors': doc.get('metadata', {}).get('authors', []),
                    'year': doc.get('metadata', {}).get('year'),
                    'relevance_score': round(score, 2),
                    'matching_keywords': list(matching_keywords)
                })

        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)

        return recommendations[:limit]

    def recommend_by_authors(
        self,
        authors: List[str],
        exclude_doc_id: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict]:
        """
        Recommande des documents par auteurs.

        Args:
            authors: Liste d'auteurs
            exclude_doc_id: Document à exclure
            limit: Nombre de recommandations

        Returns:
            Liste de recommandations
        """
        recommendations = []
        authors_lower = [a.lower() for a in authors]

        for doc_id, doc in self.documents.items():
            if doc_id == exclude_doc_id:
                continue

            doc_authors = [a.lower() for a in doc.get('metadata', {}).get('authors', [])]
            common_authors = set(authors_lower).intersection(set(doc_authors))

            if common_authors:
                recommendations.append({
                    'document_id': doc_id,
                    'title': doc.get('metadata', {}).get('title', doc['filename']),
                    'authors': doc.get('metadata', {}).get('authors', []),
                    'year': doc.get('metadata', {}).get('year'),
                    'common_authors': list(common_authors),
                    'author_match_score': len(common_authors) / len(authors_lower)
                })

        recommendations.sort(key=lambda x: x['author_match_score'], reverse=True)

        return recommendations[:limit]

    def _recommend_popular(self, limit: int = 5) -> List[Dict]:
        """Recommande les documents les plus récents ou avec plus de contenu."""
        recommendations = []

        for doc_id, doc in self.documents.items():
            # Score basé sur plusieurs critères
            score = 0

            # Documents récents
            year = doc.get('metadata', {}).get('year', 0)
            if year >= 2020:
                score += 3
            elif year >= 2015:
                score += 2
            elif year >= 2010:
                score += 1

            # Documents avec beaucoup de contenu
            num_pages = doc.get('num_pages', 0)
            if num_pages >= 20:
                score += 2
            elif num_pages >= 10:
                score += 1

            # Documents avec figures/tableaux
            num_figures = len(doc.get('figures', []))
            num_tables = len(doc.get('tables', []))
            score += min(num_figures + num_tables, 5) * 0.5

            recommendations.append({
                'document_id': doc_id,
                'title': doc.get('metadata', {}).get('title', doc['filename']),
                'authors': doc.get('metadata', {}).get('authors', []),
                'year': year,
                'popularity_score': round(score, 2)
            })

        recommendations.sort(key=lambda x: x['popularity_score'], reverse=True)

        return recommendations[:limit]

    def _calculate_similarity(self, doc1: Dict, doc2: Dict) -> float:
        """Calcule la similarité entre deux documents."""
        score = 0.0

        # Similarité des mots-clés (poids: 30%)
        keywords1 = set(k.lower() for k in doc1.get('metadata', {}).get('keywords', []))
        keywords2 = set(k.lower() for k in doc2.get('metadata', {}).get('keywords', []))

        if keywords1 and keywords2:
            keyword_similarity = len(keywords1.intersection(keywords2)) / len(keywords1.union(keywords2))
            score += keyword_similarity * 0.3

        # Similarité des auteurs (poids: 20%)
        authors1 = set(a.lower() for a in doc1.get('metadata', {}).get('authors', []))
        authors2 = set(a.lower() for a in doc2.get('metadata', {}).get('authors', []))

        if authors1 and authors2:
            author_similarity = len(authors1.intersection(authors2)) / len(authors1.union(authors2))
            score += author_similarity * 0.2

        # Similarité temporelle (poids: 10%)
        year1 = doc1.get('metadata', {}).get('year')
        year2 = doc2.get('metadata', {}).get('year')

        if year1 and year2:
            year_diff = abs(year1 - year2)
            year_similarity = max(0, 1 - (year_diff / 10))  # Décroissance sur 10 ans
            score += year_similarity * 0.1

        # Similarité du contenu (poids: 40%)
        text1 = doc1.get('full_text', '').lower()
        text2 = doc2.get('full_text', '').lower()

        # Utiliser les mots significatifs (> 4 caractères)
        words1 = set(w for w in re.findall(r'\b\w+\b', text1) if len(w) > 4)
        words2 = set(w for w in re.findall(r'\b\w+\b', text2) if len(w) > 4)

        if words1 and words2:
            # Jaccard similarity
            content_similarity = len(words1.intersection(words2)) / len(words1.union(words2))
            score += content_similarity * 0.4

        return score

    def _explain_similarity(self, doc1: Dict, doc2: Dict) -> List[str]:
        """Explique pourquoi deux documents sont similaires."""
        reasons = []

        # Auteurs communs
        authors1 = set(a.lower() for a in doc1.get('metadata', {}).get('authors', []))
        authors2 = set(a.lower() for a in doc2.get('metadata', {}).get('authors', []))
        common_authors = authors1.intersection(authors2)

        if common_authors:
            reasons.append(f"Auteurs communs : {', '.join(list(common_authors)[:3])}")

        # Mots-clés communs
        keywords1 = set(k.lower() for k in doc1.get('metadata', {}).get('keywords', []))
        keywords2 = set(k.lower() for k in doc2.get('metadata', {}).get('keywords', []))
        common_keywords = keywords1.intersection(keywords2)

        if common_keywords:
            reasons.append(f"Mots-clés communs : {', '.join(list(common_keywords)[:3])}")

        # Année proche
        year1 = doc1.get('metadata', {}).get('year')
        year2 = doc2.get('metadata', {}).get('year')

        if year1 and year2 and abs(year1 - year2) <= 2:
            reasons.append(f"Publiés à des dates proches ({year1}, {year2})")

        # Contenu similaire
        if not reasons:
            reasons.append("Contenu thématique similaire")

        return reasons

    def get_trending_topics(self, limit: int = 10) -> List[Dict]:
        """Identifie les sujets tendances dans la collection."""
        all_keywords = []

        for doc in self.documents.values():
            keywords = doc.get('metadata', {}).get('keywords', [])
            all_keywords.extend([k.lower() for k in keywords])

        keyword_counter = Counter(all_keywords)

        return [
            {'topic': keyword, 'frequency': count}
            for keyword, count in keyword_counter.most_common(limit)
        ]

    def get_author_network(self) -> Dict:
        """Génère un réseau d'auteurs collaborateurs."""
        author_connections = {}

        for doc in self.documents.values():
            authors = doc.get('metadata', {}).get('authors', [])

            # Pour chaque paire d'auteurs dans un document
            for i, author1 in enumerate(authors):
                if author1 not in author_connections:
                    author_connections[author1] = {'collaborators': Counter(), 'documents': 0}

                author_connections[author1]['documents'] += 1

                for author2 in authors[i + 1:]:
                    author_connections[author1]['collaborators'][author2] += 1

        # Convertir en format exploitable
        network = []
        for author, data in author_connections.items():
            network.append({
                'author': author,
                'total_documents': data['documents'],
                'top_collaborators': [
                    {'author': collab, 'collaborations': count}
                    for collab, count in data['collaborators'].most_common(5)
                ]
            })

        network.sort(key=lambda x: x['total_documents'], reverse=True)

        return {'authors': network[:20]}  # Top 20 auteurs
