"""
Gestionnaire des annotations pour les documents PDF.
"""
import json
import os
from typing import List, Optional
from datetime import datetime
import uuid

from app.models.annotation import Annotation, AnnotationCreate, AnnotationUpdate

class AnnotationManager:
    """Gestionnaire pour sauvegarder et récupérer les annotations."""

    def __init__(self, storage_dir: str = "../data/annotations"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def _get_annotations_file(self, document_id: str) -> str:
        """Retourne le chemin du fichier d'annotations pour un document."""
        return os.path.join(self.storage_dir, f"{document_id}.json")

    def _load_annotations(self, document_id: str) -> List[dict]:
        """Charge les annotations d'un document."""
        file_path = self._get_annotations_file(document_id)

        if not os.path.exists(file_path):
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_annotations(self, document_id: str, annotations: List[dict]):
        """Sauvegarde les annotations d'un document."""
        file_path = self._get_annotations_file(document_id)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(annotations, f, ensure_ascii=False, indent=2, default=str)

    def create_annotation(self, data: AnnotationCreate) -> Annotation:
        """Crée une nouvelle annotation."""
        annotations = self._load_annotations(data.document_id)

        annotation = Annotation(
            id=str(uuid.uuid4()),
            document_id=data.document_id,
            page=data.page,
            content=data.content,
            annotation_type=data.annotation_type,
            color=data.color,
            position=data.position,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        annotations.append(annotation.model_dump())
        self._save_annotations(data.document_id, annotations)

        return annotation

    def get_annotations(
        self,
        document_id: str,
        page: Optional[int] = None
    ) -> List[Annotation]:
        """Récupère les annotations d'un document."""
        annotations = self._load_annotations(document_id)

        if page is not None:
            annotations = [a for a in annotations if a['page'] == page]

        return [Annotation(**a) for a in annotations]

    def get_annotation(self, document_id: str, annotation_id: str) -> Optional[Annotation]:
        """Récupère une annotation spécifique."""
        annotations = self._load_annotations(document_id)

        for a in annotations:
            if a['id'] == annotation_id:
                return Annotation(**a)

        return None

    def update_annotation(
        self,
        document_id: str,
        annotation_id: str,
        data: AnnotationUpdate
    ) -> Optional[Annotation]:
        """Met à jour une annotation."""
        annotations = self._load_annotations(document_id)

        for i, a in enumerate(annotations):
            if a['id'] == annotation_id:
                # Mettre à jour les champs fournis
                if data.content is not None:
                    a['content'] = data.content
                if data.color is not None:
                    a['color'] = data.color
                if data.position is not None:
                    a['position'] = data.position

                a['updated_at'] = datetime.now()

                annotations[i] = a
                self._save_annotations(document_id, annotations)

                return Annotation(**a)

        return None

    def delete_annotation(self, document_id: str, annotation_id: str) -> bool:
        """Supprime une annotation."""
        annotations = self._load_annotations(document_id)

        original_count = len(annotations)
        annotations = [a for a in annotations if a['id'] != annotation_id]

        if len(annotations) < original_count:
            self._save_annotations(document_id, annotations)
            return True

        return False

    def export_annotations(self, document_id: str) -> dict:
        """Exporte toutes les annotations d'un document."""
        annotations = self._load_annotations(document_id)

        return {
            "document_id": document_id,
            "annotations": annotations,
            "exported_at": datetime.now().isoformat()
        }
