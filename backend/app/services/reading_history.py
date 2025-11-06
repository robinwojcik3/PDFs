"""
Gestionnaire d'historique de lecture des documents.
"""
import json
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class ReadingHistory:
    """Gestionnaire d'historique de lecture."""

    def __init__(self, storage_dir: str = "../data/history"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self.history_file = os.path.join(self.storage_dir, "reading_history.json")

        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Crée le fichier d'historique s'il n'existe pas."""
        if not os.path.exists(self.history_file):
            self._save_history({})

    def _load_history(self) -> Dict:
        """Charge l'historique depuis le fichier."""
        with open(self.history_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_history(self, history: Dict):
        """Sauvegarde l'historique dans le fichier."""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2, default=str)

    def record_view(
        self,
        document_id: str,
        page: Optional[int] = None,
        duration_seconds: Optional[int] = None
    ) -> Dict:
        """
        Enregistre une consultation de document.

        Args:
            document_id: ID du document
            page: Page consultée (optionnel)
            duration_seconds: Durée de lecture en secondes (optionnel)

        Returns:
            Enregistrement créé
        """
        history = self._load_history()

        if document_id not in history:
            history[document_id] = {
                'document_id': document_id,
                'first_view': datetime.now(),
                'last_view': datetime.now(),
                'total_views': 0,
                'total_time_seconds': 0,
                'pages_read': set(),
                'current_page': 1,
                'progress_percent': 0,
                'sessions': []
            }

        doc_history = history[document_id]

        # Convertir les sets en listes pour la sérialisation
        if isinstance(doc_history['pages_read'], list):
            doc_history['pages_read'] = set(doc_history['pages_read'])

        # Mettre à jour les statistiques
        doc_history['last_view'] = datetime.now()
        doc_history['total_views'] += 1

        if duration_seconds:
            doc_history['total_time_seconds'] += duration_seconds

        if page:
            doc_history['pages_read'].add(page)
            doc_history['current_page'] = page

        # Enregistrer la session
        session = {
            'timestamp': datetime.now(),
            'page': page,
            'duration_seconds': duration_seconds or 0
        }
        doc_history['sessions'].append(session)

        # Reconvertir en liste pour la sauvegarde
        doc_history['pages_read'] = list(doc_history['pages_read'])

        history[document_id] = doc_history
        self._save_history(history)

        return session

    def update_progress(
        self,
        document_id: str,
        current_page: int,
        total_pages: int
    ) -> Dict:
        """
        Met à jour la progression de lecture.

        Args:
            document_id: ID du document
            current_page: Page actuelle
            total_pages: Nombre total de pages

        Returns:
            Historique mis à jour
        """
        history = self._load_history()

        if document_id in history:
            doc_history = history[document_id]

            # Convertir en set si nécessaire
            if isinstance(doc_history['pages_read'], list):
                doc_history['pages_read'] = set(doc_history['pages_read'])

            doc_history['current_page'] = current_page
            doc_history['pages_read'].add(current_page)

            # Calculer le pourcentage de progression
            pages_read_count = len(doc_history['pages_read'])
            doc_history['progress_percent'] = int((pages_read_count / total_pages) * 100) if total_pages > 0 else 0

            # Reconvertir en liste
            doc_history['pages_read'] = list(doc_history['pages_read'])

            history[document_id] = doc_history
            self._save_history(history)

            return doc_history

        return None

    def get_history(self, document_id: str) -> Optional[Dict]:
        """Récupère l'historique d'un document."""
        history = self._load_history()
        return history.get(document_id)

    def get_all_history(
        self,
        sort_by: str = 'last_view',
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Récupère tout l'historique.

        Args:
            sort_by: Tri par 'last_view', 'total_views' ou 'total_time_seconds'
            limit: Limite du nombre de résultats

        Returns:
            Liste d'historiques triés
        """
        history = self._load_history()
        history_list = list(history.values())

        # Convertir les chaînes de dates en objets datetime pour le tri
        for item in history_list:
            if isinstance(item.get('last_view'), str):
                item['last_view'] = datetime.fromisoformat(item['last_view'])
            if isinstance(item.get('first_view'), str):
                item['first_view'] = datetime.fromisoformat(item['first_view'])

        if sort_by == 'last_view':
            history_list.sort(key=lambda x: x['last_view'], reverse=True)
        elif sort_by == 'total_views':
            history_list.sort(key=lambda x: x['total_views'], reverse=True)
        elif sort_by == 'total_time_seconds':
            history_list.sort(key=lambda x: x['total_time_seconds'], reverse=True)

        if limit:
            history_list = history_list[:limit]

        return history_list

    def get_recent_documents(self, days: int = 7, limit: int = 10) -> List[Dict]:
        """
        Récupère les documents récemment consultés.

        Args:
            days: Nombre de jours à considérer
            limit: Nombre maximum de documents

        Returns:
            Liste de documents récents
        """
        history = self._load_history()
        cutoff_date = datetime.now() - timedelta(days=days)

        recent = []

        for doc_id, doc_history in history.items():
            last_view = doc_history['last_view']
            if isinstance(last_view, str):
                last_view = datetime.fromisoformat(last_view)

            if last_view >= cutoff_date:
                recent.append(doc_history)

        # Trier par date de dernière consultation
        recent.sort(key=lambda x: x['last_view'] if isinstance(x['last_view'], datetime) else datetime.fromisoformat(x['last_view']), reverse=True)

        return recent[:limit]

    def get_reading_statistics(self) -> Dict:
        """Retourne des statistiques globales de lecture."""
        history = self._load_history()

        if not history:
            return {
                'total_documents_read': 0,
                'total_reading_time_hours': 0,
                'total_views': 0,
                'average_time_per_document': 0,
                'most_read_document': None,
                'longest_reading_session': None
            }

        total_time = sum(doc['total_time_seconds'] for doc in history.values())
        total_views = sum(doc['total_views'] for doc in history.values())

        most_read = max(history.values(), key=lambda x: x['total_views'])

        # Trouver la session la plus longue
        longest_session = None
        max_duration = 0

        for doc in history.values():
            for session in doc.get('sessions', []):
                if session['duration_seconds'] > max_duration:
                    max_duration = session['duration_seconds']
                    longest_session = {
                        'document_id': doc['document_id'],
                        'duration_seconds': session['duration_seconds'],
                        'timestamp': session['timestamp']
                    }

        return {
            'total_documents_read': len(history),
            'total_reading_time_hours': round(total_time / 3600, 2),
            'total_reading_time_formatted': self._format_duration(total_time),
            'total_views': total_views,
            'average_time_per_document': round(total_time / len(history), 0) if history else 0,
            'average_views_per_document': round(total_views / len(history), 1) if history else 0,
            'most_read_document': {
                'document_id': most_read['document_id'],
                'total_views': most_read['total_views'],
                'total_time': most_read['total_time_seconds']
            },
            'longest_reading_session': longest_session
        }

    def get_reading_by_period(self, period: str = 'week') -> Dict:
        """
        Retourne les statistiques de lecture par période.

        Args:
            period: 'day', 'week', 'month'

        Returns:
            Statistiques par période
        """
        history = self._load_history()

        if period == 'day':
            delta = timedelta(days=1)
            periods_count = 7  # Derniers 7 jours
        elif period == 'week':
            delta = timedelta(weeks=1)
            periods_count = 4  # Dernières 4 semaines
        else:  # month
            delta = timedelta(days=30)
            periods_count = 6  # Derniers 6 mois

        now = datetime.now()
        periods_data = []

        for i in range(periods_count):
            period_end = now - (delta * i)
            period_start = period_end - delta

            views = 0
            time_seconds = 0
            documents = set()

            for doc in history.values():
                for session in doc.get('sessions', []):
                    session_time = session['timestamp']
                    if isinstance(session_time, str):
                        session_time = datetime.fromisoformat(session_time)

                    if period_start <= session_time < period_end:
                        views += 1
                        time_seconds += session['duration_seconds']
                        documents.add(doc['document_id'])

            periods_data.append({
                'period': f"{period_start.strftime('%Y-%m-%d')} - {period_end.strftime('%Y-%m-%d')}",
                'views': views,
                'time_hours': round(time_seconds / 3600, 2),
                'documents_count': len(documents)
            })

        periods_data.reverse()  # Ordre chronologique
        return {'periods': periods_data}

    def _format_duration(self, seconds: int) -> str:
        """Formate une durée en secondes en format lisible."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"

    def clear_history(self, document_id: Optional[str] = None) -> bool:
        """
        Efface l'historique.

        Args:
            document_id: Si fourni, efface seulement ce document, sinon tout

        Returns:
            Succès de l'opération
        """
        if document_id:
            history = self._load_history()
            if document_id in history:
                del history[document_id]
                self._save_history(history)
                return True
            return False
        else:
            self._save_history({})
            return True
