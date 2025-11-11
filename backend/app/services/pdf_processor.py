"""
Service de traitement et d'extraction de contenu des PDFs.
"""
import os
import re
import io
import hashlib
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from PIL import Image
import pypdf
import pdfplumber

from app.models.document import Document, DocumentMetadata, Figure, Table, Section

class PDFProcessor:
    """Processeur pour extraire le contenu des PDFs."""

    def __init__(self, pdf_dir: str = "../data/pdfs", extract_dir: str = "../data/extracted"):
        self.pdf_dir = pdf_dir
        self.extract_dir = extract_dir
        os.makedirs(self.extract_dir, exist_ok=True)

    def process_pdf(self, filename: str) -> Document:
        """
        Traite un PDF et extrait tout son contenu.

        Args:
            filename: Nom du fichier PDF

        Returns:
            Document indexé avec tout le contenu extrait
        """
        pdf_path = os.path.join(self.pdf_dir, filename)

        # Générer un ID unique pour le document
        doc_id = self._generate_document_id(filename)

        # Créer un dossier pour les extractions de ce document
        doc_extract_dir = os.path.join(self.extract_dir, doc_id)
        os.makedirs(doc_extract_dir, exist_ok=True)

        # Extraire les métadonnées
        metadata = self._extract_metadata(pdf_path)

        # Extraire le texte complet
        full_text = self._extract_full_text(pdf_path)

        # Extraire les sections
        sections = self._extract_sections(pdf_path, full_text)

        # Extraire les figures
        figures = self._extract_figures(pdf_path, doc_id, doc_extract_dir)

        # Extraire les tableaux
        tables = self._extract_tables(pdf_path)

        # Obtenir le nombre de pages et la taille du fichier
        with open(pdf_path, 'rb') as f:
            pdf_reader = pypdf.PdfReader(f)
            num_pages = len(pdf_reader.pages)

        file_size = os.path.getsize(pdf_path)

        return Document(
            id=doc_id,
            filename=filename,
            path=pdf_path,
            num_pages=num_pages,
            metadata=metadata,
            sections=sections,
            figures=figures,
            tables=tables,
            full_text=full_text,
            indexed_at=datetime.now(),
            file_size=file_size
        )

    def _generate_document_id(self, filename: str) -> str:
        """Génère un ID unique pour le document."""
        return hashlib.md5(filename.encode()).hexdigest()[:16]

    def _extract_metadata(self, pdf_path: str) -> DocumentMetadata:
        """Extrait les métadonnées du PDF."""
        metadata = DocumentMetadata()

        try:
            with open(pdf_path, 'rb') as f:
                pdf_reader = pypdf.PdfReader(f)
                pdf_metadata = pdf_reader.metadata

                if pdf_metadata:
                    # Titre
                    if '/Title' in pdf_metadata and pdf_metadata['/Title']:
                        metadata.title = str(pdf_metadata['/Title'])

                    # Auteur(s)
                    if '/Author' in pdf_metadata and pdf_metadata['/Author']:
                        authors_str = str(pdf_metadata['/Author'])
                        metadata.authors = [a.strip() for a in authors_str.split(',')]

                    # Keywords
                    if '/Keywords' in pdf_metadata and pdf_metadata['/Keywords']:
                        keywords_str = str(pdf_metadata['/Keywords'])
                        metadata.keywords = [k.strip() for k in keywords_str.split(',')]
        except Exception as e:
            print(f"Erreur lors de l'extraction des métadonnées: {e}")

        # Si pas de titre dans les métadonnées, utiliser le nom du fichier
        if not metadata.title:
            metadata.title = os.path.splitext(os.path.basename(pdf_path))[0]

        return metadata

    def _extract_full_text(self, pdf_path: str) -> str:
        """Extrait tout le texte du PDF."""
        text_parts = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
        except Exception as e:
            print(f"Erreur lors de l'extraction du texte: {e}")

        return "\n\n".join(text_parts)

    def _extract_sections(self, pdf_path: str, full_text: str) -> List[Section]:
        """Extrait les sections du document."""
        sections = []

        # Patterns pour détecter les titres de sections
        section_patterns = [
            r'^(\d+\.?\s+)?([A-Z][A-Z\s]+)$',  # TITRE EN MAJUSCULES
            r'^(\d+\.?\s+)([A-Z][a-zA-Z\s]+)$',  # 1. Titre avec numéro
        ]

        lines = full_text.split('\n')
        current_section = None
        current_content = []
        section_id = 0

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Vérifier si la ligne est un titre de section
            is_section_title = False
            for pattern in section_patterns:
                if re.match(pattern, line) and len(line) < 100:
                    is_section_title = True
                    break

            if is_section_title:
                # Sauvegarder la section précédente
                if current_section:
                    sections.append(Section(
                        id=f"section_{section_id}",
                        title=current_section,
                        content="\n".join(current_content),
                        page_start=1,  # Approximation
                        page_end=1,
                        level=1
                    ))
                    section_id += 1

                # Commencer une nouvelle section
                current_section = line
                current_content = []
            else:
                current_content.append(line)

        # Ajouter la dernière section
        if current_section:
            sections.append(Section(
                id=f"section_{section_id}",
                title=current_section,
                content="\n".join(current_content),
                page_start=1,
                page_end=1,
                level=1
            ))

        return sections

    def _extract_figures(self, pdf_path: str, doc_id: str, extract_dir: str) -> List[Figure]:
        """Extrait les figures du PDF."""
        figures = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extraire les images de la page
                    images = page.images

                    for img_idx, img in enumerate(images):
                        try:
                            # Créer un nom de fichier pour l'image
                            fig_id = f"fig_{page_num}_{img_idx}"
                            img_filename = f"{fig_id}.png"
                            img_path = os.path.join(extract_dir, img_filename)

                            # Extraire et sauvegarder l'image
                            # Note: Cette partie est simplifiée, pdfplumber nécessite
                            # un traitement plus complexe pour extraire les images

                            # Pour l'instant, on enregistre juste les métadonnées
                            figures.append(Figure(
                                id=fig_id,
                                page=page_num,
                                path=f"/static/extracted/{doc_id}/{img_filename}",
                                caption=f"Figure {len(figures) + 1}",
                                width=int(img.get('width', 0)),
                                height=int(img.get('height', 0))
                            ))
                        except Exception as e:
                            print(f"Erreur lors de l'extraction de l'image {img_idx} page {page_num}: {e}")
        except Exception as e:
            print(f"Erreur lors de l'extraction des figures: {e}")

        return figures

    def _extract_tables(self, pdf_path: str) -> List[Table]:
        """Extrait les tableaux du PDF."""
        tables = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extraire les tableaux de la page
                    page_tables = page.extract_tables()

                    for table_idx, table_data in enumerate(page_tables):
                        if table_data and len(table_data) > 0:
                            tables.append(Table(
                                id=f"table_{page_num}_{table_idx}",
                                page=page_num,
                                data=table_data,
                                caption=f"Tableau {len(tables) + 1}"
                            ))
        except Exception as e:
            print(f"Erreur lors de l'extraction des tableaux: {e}")

        return tables

    def list_pdfs(self) -> List[str]:
        """Liste tous les PDFs disponibles dans le dossier."""
        if not os.path.exists(self.pdf_dir):
            return []

        return [f for f in os.listdir(self.pdf_dir) if f.lower().endswith('.pdf')]
