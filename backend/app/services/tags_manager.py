"""
Gestionnaire de tags et catégories pour les documents.
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from collections import Counter

class TagsManager:
    """Gestionnaire de tags et catégories."""

    def __init__(self, storage_dir: str = "../data/tags"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self.tags_file = os.path.join(self.storage_dir, "tags.json")
        self.categories_file = os.path.join(self.storage_dir, "categories.json")

        # Catégories scientifiques prédéfinies
        self.predefined_categories = {
            'domaine': [
                'Informatique', 'Mathématiques', 'Physique', 'Chimie', 'Biologie',
                'Médecine', 'Ingénierie', 'Sciences sociales', 'Économie', 'Psychologie'
            ],
            'type': [
                'Article de recherche', 'Revue de littérature', 'Étude de cas',
                'Méta-analyse', 'Thèse', 'Rapport technique', 'Conférence'
            ],
            'methodologie': [
                'Expérimentale', 'Quantitative', 'Qualitative', 'Théorique',
                'Computationnelle', 'Empirique', 'Comparative'
            ],
            'statut': [
                'À lire', 'En cours', 'Lu', 'À réviser', 'Référence'
            ]
        }

        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Crée les fichiers de stockage s'ils n'existent pas."""
        if not os.path.exists(self.tags_file):
            self._save_tags({})

        if not os.path.exists(self.categories_file):
            self._save_categories({})

    def _load_tags(self) -> Dict:
        """Charge les tags depuis le fichier."""
        with open(self.tags_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_tags(self, tags: Dict):
        """Sauvegarde les tags dans le fichier."""
        with open(self.tags_file, 'w', encoding='utf-8') as f:
            json.dump(tags, f, ensure_ascii=False, indent=2)

    def _load_categories(self) -> Dict:
        """Charge les catégories depuis le fichier."""
        with open(self.categories_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_categories(self, categories: Dict):
        """Sauvegarde les catégories dans le fichier."""
        with open(self.categories_file, 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)

    def add_tag(self, document_id: str, tag: str, color: str = None) -> Dict:
        """
        Ajoute un tag à un document.

        Args:
            document_id: ID du document
            tag: Nom du tag
            color: Couleur du tag (optionnel)

        Returns:
            Tag créé
        """
        tags = self._load_tags()

        if document_id not in tags:
            tags[document_id] = []

        # Vérifier si le tag n'existe pas déjà
        if not any(t['name'].lower() == tag.lower() for t in tags[document_id]):
            tag_data = {
                'name': tag,
                'color': color or self._generate_tag_color(tag),
                'created_at': datetime.now().isoformat()
            }
            tags[document_id].append(tag_data)
            self._save_tags(tags)

            return tag_data

        return None

    def remove_tag(self, document_id: str, tag: str) -> bool:
        """Supprime un tag d'un document."""
        tags = self._load_tags()

        if document_id in tags:
            original_count = len(tags[document_id])
            tags[document_id] = [t for t in tags[document_id] if t['name'].lower() != tag.lower()]

            if len(tags[document_id]) < original_count:
                self._save_tags(tags)
                return True

        return False

    def get_tags(self, document_id: str) -> List[Dict]:
        """Récupère tous les tags d'un document."""
        tags = self._load_tags()
        return tags.get(document_id, [])

    def get_all_tags(self) -> List[Dict]:
        """Récupère tous les tags utilisés avec leur fréquence."""
        tags = self._load_tags()
        tag_counter = Counter()

        for doc_tags in tags.values():
            for tag in doc_tags:
                tag_counter[tag['name']] += 1

        return [
            {'name': name, 'count': count}
            for name, count in tag_counter.most_common()
        ]

    def search_by_tags(self, tag_names: List[str], match_all: bool = False) -> List[str]:
        """
        Recherche des documents par tags.

        Args:
            tag_names: Liste de noms de tags
            match_all: Si True, le document doit avoir tous les tags

        Returns:
            Liste d'IDs de documents
        """
        tags = self._load_tags()
        matching_docs = []

        for doc_id, doc_tags in tags.items():
            doc_tag_names = {t['name'].lower() for t in doc_tags}
            search_tag_names = {t.lower() for t in tag_names}

            if match_all:
                if search_tag_names.issubset(doc_tag_names):
                    matching_docs.append(doc_id)
            else:
                if search_tag_names.intersection(doc_tag_names):
                    matching_docs.append(doc_id)

        return matching_docs

    def set_category(self, document_id: str, category_type: str, category_value: str) -> Dict:
        """
        Définit une catégorie pour un document.

        Args:
            document_id: ID du document
            category_type: Type de catégorie (domaine, type, etc.)
            category_value: Valeur de la catégorie

        Returns:
            Catégorie définie
        """
        categories = self._load_categories()

        if document_id not in categories:
            categories[document_id] = {}

        categories[document_id][category_type] = {
            'value': category_value,
            'updated_at': datetime.now().isoformat()
        }

        self._save_categories(categories)

        return categories[document_id][category_type]

    def get_categories(self, document_id: str) -> Dict:
        """Récupère toutes les catégories d'un document."""
        categories = self._load_categories()
        return categories.get(document_id, {})

    def get_predefined_categories(self) -> Dict[str, List[str]]:
        """Retourne les catégories prédéfinies."""
        return self.predefined_categories

    def get_documents_by_category(self, category_type: str, category_value: str) -> List[str]:
        """Récupère les documents d'une catégorie donnée."""
        categories = self._load_categories()
        matching_docs = []

        for doc_id, doc_categories in categories.items():
            if category_type in doc_categories:
                if doc_categories[category_type]['value'] == category_value:
                    matching_docs.append(doc_id)

        return matching_docs

    def suggest_tags(self, document_keywords: List[str], existing_tags: List[str]) -> List[str]:
        """
        Suggère des tags basés sur les mots-clés du document.

        Args:
            document_keywords: Mots-clés extraits du document
            existing_tags: Tags déjà appliqués

        Returns:
            Suggestions de tags
        """
        all_tags = self.get_all_tags()
        suggestions = []

        # Tags basés sur les mots-clés
        for keyword in document_keywords[:10]:  # Top 10 keywords
            keyword_lower = keyword.lower()

            # Vérifier si le mot-clé n'est pas déjà un tag
            if keyword_lower not in [t.lower() for t in existing_tags]:
                suggestions.append(keyword)

        # Tags populaires similaires
        for tag_data in all_tags[:20]:  # Top 20 tags
            tag_name = tag_data['name']
            if tag_name not in existing_tags and tag_name not in suggestions:
                # Vérifier la similarité avec les mots-clés
                if any(keyword.lower() in tag_name.lower() or tag_name.lower() in keyword.lower()
                       for keyword in document_keywords):
                    suggestions.append(tag_name)

        return suggestions[:10]  # Max 10 suggestions

    def _generate_tag_color(self, tag: str) -> str:
        """Génère une couleur pour un tag basée sur son nom."""
        # Hash simple du nom pour générer une couleur
        hash_value = sum(ord(c) for c in tag)

        colors = [
            '#3b82f6',  # blue
            '#8b5cf6',  # purple
            '#ec4899',  # pink
            '#f59e0b',  # amber
            '#10b981',  # green
            '#06b6d4',  # cyan
            '#f97316',  # orange
            '#6366f1',  # indigo
            '#14b8a6',  # teal
            '#a855f7',  # violet
        ]

        return colors[hash_value % len(colors)]

    def get_tag_statistics(self) -> Dict:
        """Retourne des statistiques sur l'utilisation des tags."""
        tags = self._load_tags()
        categories = self._load_categories()

        tag_counter = Counter()
        category_counter = {}

        for doc_tags in tags.values():
            for tag in doc_tags:
                tag_counter[tag['name']] += 1

        for doc_categories in categories.values():
            for cat_type, cat_data in doc_categories.items():
                if cat_type not in category_counter:
                    category_counter[cat_type] = Counter()
                category_counter[cat_type][cat_data['value']] += 1

        return {
            'total_documents_with_tags': len(tags),
            'total_unique_tags': len(tag_counter),
            'most_used_tags': dict(tag_counter.most_common(10)),
            'tags_per_document': len(tag_counter) / len(tags) if tags else 0,
            'category_distribution': {
                cat_type: dict(counter.most_common())
                for cat_type, counter in category_counter.items()
            }
        }
