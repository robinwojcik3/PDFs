"""
Gestionnaire de collections et favoris de documents.
"""
import json
import os
import uuid
from typing import List, Dict, Optional
from datetime import datetime

class CollectionsManager:
    """Gestionnaire de collections et favoris."""

    def __init__(self, storage_dir: str = "../data/collections"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self.collections_file = os.path.join(self.storage_dir, "collections.json")
        self.favorites_file = os.path.join(self.storage_dir, "favorites.json")

        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Crée les fichiers de stockage s'ils n'existent pas."""
        if not os.path.exists(self.collections_file):
            self._save_collections([])

        if not os.path.exists(self.favorites_file):
            self._save_favorites({})

    def _load_collections(self) -> List[Dict]:
        """Charge les collections depuis le fichier."""
        with open(self.collections_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_collections(self, collections: List[Dict]):
        """Sauvegarde les collections dans le fichier."""
        with open(self.collections_file, 'w', encoding='utf-8') as f:
            json.dump(collections, f, ensure_ascii=False, indent=2, default=str)

    def _load_favorites(self) -> Dict:
        """Charge les favoris depuis le fichier."""
        with open(self.favorites_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_favorites(self, favorites: Dict):
        """Sauvegarde les favoris dans le fichier."""
        with open(self.favorites_file, 'w', encoding='utf-8') as f:
            json.dump(favorites, f, ensure_ascii=False, indent=2, default=str)

    # === Collections ===

    def create_collection(
        self,
        name: str,
        description: str = "",
        color: str = "#3b82f6",
        icon: str = "folder"
    ) -> Dict:
        """
        Crée une nouvelle collection.

        Args:
            name: Nom de la collection
            description: Description
            color: Couleur de la collection
            icon: Icône de la collection

        Returns:
            Collection créée
        """
        collections = self._load_collections()

        collection = {
            'id': str(uuid.uuid4()),
            'name': name,
            'description': description,
            'color': color,
            'icon': icon,
            'documents': [],
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

        collections.append(collection)
        self._save_collections(collections)

        return collection

    def get_collections(self) -> List[Dict]:
        """Récupère toutes les collections."""
        return self._load_collections()

    def get_collection(self, collection_id: str) -> Optional[Dict]:
        """Récupère une collection spécifique."""
        collections = self._load_collections()

        for collection in collections:
            if collection['id'] == collection_id:
                return collection

        return None

    def update_collection(
        self,
        collection_id: str,
        name: str = None,
        description: str = None,
        color: str = None,
        icon: str = None
    ) -> Optional[Dict]:
        """Met à jour une collection."""
        collections = self._load_collections()

        for i, collection in enumerate(collections):
            if collection['id'] == collection_id:
                if name:
                    collection['name'] = name
                if description is not None:
                    collection['description'] = description
                if color:
                    collection['color'] = color
                if icon:
                    collection['icon'] = icon

                collection['updated_at'] = datetime.now()
                collections[i] = collection
                self._save_collections(collections)

                return collection

        return None

    def delete_collection(self, collection_id: str) -> bool:
        """Supprime une collection."""
        collections = self._load_collections()
        original_count = len(collections)

        collections = [c for c in collections if c['id'] != collection_id]

        if len(collections) < original_count:
            self._save_collections(collections)
            return True

        return False

    def add_document_to_collection(self, collection_id: str, document_id: str) -> bool:
        """Ajoute un document à une collection."""
        collections = self._load_collections()

        for i, collection in enumerate(collections):
            if collection['id'] == collection_id:
                if document_id not in collection['documents']:
                    collection['documents'].append(document_id)
                    collection['updated_at'] = datetime.now()
                    collections[i] = collection
                    self._save_collections(collections)
                    return True

        return False

    def remove_document_from_collection(self, collection_id: str, document_id: str) -> bool:
        """Retire un document d'une collection."""
        collections = self._load_collections()

        for i, collection in enumerate(collections):
            if collection['id'] == collection_id:
                if document_id in collection['documents']:
                    collection['documents'].remove(document_id)
                    collection['updated_at'] = datetime.now()
                    collections[i] = collection
                    self._save_collections(collections)
                    return True

        return False

    def get_document_collections(self, document_id: str) -> List[Dict]:
        """Récupère toutes les collections contenant un document."""
        collections = self._load_collections()

        return [
            collection for collection in collections
            if document_id in collection['documents']
        ]

    # === Favoris ===

    def add_favorite(
        self,
        document_id: str,
        priority: int = 3,
        notes: str = ""
    ) -> Dict:
        """
        Ajoute un document aux favoris.

        Args:
            document_id: ID du document
            priority: Priorité (1-5, 5 = haute)
            notes: Notes personnelles

        Returns:
            Favori créé
        """
        favorites = self._load_favorites()

        favorite = {
            'document_id': document_id,
            'priority': priority,
            'notes': notes,
            'added_at': datetime.now()
        }

        favorites[document_id] = favorite
        self._save_favorites(favorites)

        return favorite

    def remove_favorite(self, document_id: str) -> bool:
        """Retire un document des favoris."""
        favorites = self._load_favorites()

        if document_id in favorites:
            del favorites[document_id]
            self._save_favorites(favorites)
            return True

        return False

    def update_favorite(
        self,
        document_id: str,
        priority: int = None,
        notes: str = None
    ) -> Optional[Dict]:
        """Met à jour un favori."""
        favorites = self._load_favorites()

        if document_id in favorites:
            if priority is not None:
                favorites[document_id]['priority'] = priority
            if notes is not None:
                favorites[document_id]['notes'] = notes

            self._save_favorites(favorites)
            return favorites[document_id]

        return None

    def get_favorites(self, sort_by: str = 'priority') -> List[Dict]:
        """
        Récupère tous les favoris.

        Args:
            sort_by: Tri par 'priority', 'added_at' ou 'document_id'

        Returns:
            Liste des favoris triés
        """
        favorites = self._load_favorites()
        favorites_list = list(favorites.values())

        if sort_by == 'priority':
            favorites_list.sort(key=lambda x: x['priority'], reverse=True)
        elif sort_by == 'added_at':
            favorites_list.sort(key=lambda x: x['added_at'], reverse=True)

        return favorites_list

    def is_favorite(self, document_id: str) -> bool:
        """Vérifie si un document est en favori."""
        favorites = self._load_favorites()
        return document_id in favorites

    def get_favorite(self, document_id: str) -> Optional[Dict]:
        """Récupère un favori spécifique."""
        favorites = self._load_favorites()
        return favorites.get(document_id)

    # === Statistiques ===

    def get_statistics(self) -> Dict:
        """Retourne des statistiques sur les collections et favoris."""
        collections = self._load_collections()
        favorites = self._load_favorites()

        total_documents_in_collections = sum(len(c['documents']) for c in collections)

        priority_distribution = {}
        for fav in favorites.values():
            priority = fav['priority']
            priority_distribution[priority] = priority_distribution.get(priority, 0) + 1

        return {
            'total_collections': len(collections),
            'total_favorites': len(favorites),
            'total_documents_in_collections': total_documents_in_collections,
            'average_documents_per_collection': (
                total_documents_in_collections / len(collections)
                if collections else 0
            ),
            'largest_collection': max(
                (c for c in collections),
                key=lambda x: len(x['documents']),
                default=None
            ),
            'priority_distribution': priority_distribution,
            'collections_list': [
                {
                    'id': c['id'],
                    'name': c['name'],
                    'document_count': len(c['documents'])
                }
                for c in collections
            ]
        }
