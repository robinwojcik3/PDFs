"""
Service d'indexation et de recherche full-text.
"""
import os
import json
from typing import List, Dict
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, ID, KEYWORD, NUMERIC, STORED
from whoosh.qparser import MultifieldParser
from whoosh.query import Term, Or

from app.models.document import Document, SearchResult

class SearchIndexer:
    """Indexeur et moteur de recherche pour les documents."""

    def __init__(self, index_dir: str = "../data/index"):
        self.index_dir = index_dir
        os.makedirs(self.index_dir, exist_ok=True)

        # Définir le schéma de l'index
        self.schema = Schema(
            document_id=ID(stored=True, unique=True),
            filename=TEXT(stored=True),
            title=TEXT(stored=True),
            authors=KEYWORD(stored=True, commas=True),
            year=NUMERIC(stored=True),
            abstract=TEXT(stored=True),
            keywords=KEYWORD(stored=True, commas=True),
            full_text=TEXT(stored=True),
            sections=TEXT(stored=True),
            num_pages=NUMERIC(stored=True),
            num_figures=NUMERIC(stored=True),
            num_tables=NUMERIC(stored=True)
        )

        # Créer ou ouvrir l'index
        if not exists_in(self.index_dir):
            self.index = create_in(self.index_dir, self.schema)
        else:
            self.index = open_dir(self.index_dir)

    def index_document(self, document: Document):
        """Indexe un document pour la recherche."""
        writer = self.index.writer()

        # Préparer les données pour l'indexation
        sections_text = " ".join([s.title + " " + s.content for s in document.sections])
        authors = ", ".join(document.metadata.authors)
        keywords = ", ".join(document.metadata.keywords)

        writer.update_document(
            document_id=document.id,
            filename=document.filename,
            title=document.metadata.title or document.filename,
            authors=authors,
            year=document.metadata.year or 0,
            abstract=document.metadata.abstract or "",
            keywords=keywords,
            full_text=document.full_text,
            sections=sections_text,
            num_pages=document.num_pages,
            num_figures=len(document.figures),
            num_tables=len(document.tables)
        )

        writer.commit()

    def search(
        self,
        query: str,
        filters: Dict = None,
        limit: int = 20
    ) -> List[SearchResult]:
        """
        Effectue une recherche full-text dans les documents.

        Args:
            query: Requête de recherche
            filters: Filtres optionnels (auteur, année, etc.)
            limit: Nombre maximum de résultats

        Returns:
            Liste de résultats de recherche
        """
        results = []

        with self.index.searcher() as searcher:
            # Parser multi-champs pour chercher dans plusieurs champs
            parser = MultifieldParser(
                ["title", "full_text", "sections", "abstract", "keywords"],
                schema=self.schema
            )

            query_obj = parser.parse(query)

            # Appliquer les filtres si fournis
            if filters:
                # TODO: Implémenter les filtres (année, auteur, etc.)
                pass

            # Effectuer la recherche
            search_results = searcher.search(query_obj, limit=limit)

            for hit in search_results:
                # Extraire un snippet du texte
                snippet = hit.highlights("full_text", top=3) or hit["full_text"][:200] + "..."

                results.append(SearchResult(
                    document_id=hit["document_id"],
                    title=hit["title"],
                    filename=hit["filename"],
                    score=hit.score,
                    snippet=snippet,
                    highlight=hit.highlights("full_text")
                ))

        return results

    def get_suggestions(self, partial_query: str, limit: int = 5) -> List[str]:
        """
        Retourne des suggestions de recherche basées sur une requête partielle.

        Args:
            partial_query: Début de la requête
            limit: Nombre de suggestions

        Returns:
            Liste de suggestions
        """
        suggestions = []

        with self.index.searcher() as searcher:
            # Extraire des termes fréquents correspondants
            for fieldname in ["title", "keywords"]:
                terms = searcher.field_terms(fieldname)
                for term in terms:
                    if partial_query.lower() in term.lower():
                        suggestions.append(term)
                        if len(suggestions) >= limit:
                            break
                if len(suggestions) >= limit:
                    break

        return suggestions[:limit]

    def delete_document(self, document_id: str):
        """Supprime un document de l'index."""
        writer = self.index.writer()
        writer.delete_by_term('document_id', document_id)
        writer.commit()

    def clear_index(self):
        """Vide complètement l'index."""
        writer = self.index.writer()
        writer.commit(mergetype='CLEAR')
