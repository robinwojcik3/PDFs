"""
Service d'export de documents dans différents formats.
"""
from typing import Dict, List, Optional
from datetime import datetime
import json
import re

class DocumentExporter:
    """Exporteur de documents vers différents formats."""

    def export_to_markdown(self, document: Dict, include_annotations: bool = True, annotations: List[Dict] = None) -> str:
        """
        Exporte un document en format Markdown.

        Args:
            document: Document à exporter
            include_annotations: Inclure les annotations
            annotations: Liste d'annotations

        Returns:
            Contenu Markdown
        """
        md = []

        # En-tête
        md.append(f"# {document.get('metadata', {}).get('title', document['filename'])}\n")

        # Métadonnées
        metadata = document.get('metadata', {})

        if metadata.get('authors'):
            md.append(f"**Auteurs:** {', '.join(metadata['authors'])}\n")

        if metadata.get('year'):
            md.append(f"**Année:** {metadata['year']}\n")

        if metadata.get('keywords'):
            md.append(f"**Mots-clés:** {', '.join(metadata['keywords'])}\n")

        md.append(f"**Pages:** {document.get('num_pages', 0)}\n")

        if metadata.get('doi'):
            md.append(f"**DOI:** {metadata['doi']}\n")

        md.append("\n---\n\n")

        # Abstract
        if metadata.get('abstract'):
            md.append("## Résumé\n\n")
            md.append(f"{metadata['abstract']}\n\n")

        # Sections
        sections = document.get('sections', [])
        if sections:
            md.append("## Contenu\n\n")

            for section in sections:
                level = section.get('level', 1) + 1  # +1 car le titre principal est #
                md.append(f"{'#' * level} {section['title']}\n\n")
                md.append(f"{section['content']}\n\n")

        # Figures
        figures = document.get('figures', [])
        if figures:
            md.append("## Figures\n\n")

            for figure in figures:
                md.append(f"### {figure.get('caption', f'Figure {figure[\"id\"]}')}\n\n")
                md.append(f"![{figure.get('caption', '')}]({figure.get('path', '')})\n\n")
                md.append(f"*Page {figure.get('page')}*\n\n")

        # Tableaux
        tables = document.get('tables', [])
        if tables:
            md.append("## Tableaux\n\n")

            for table in tables:
                md.append(f"### {table.get('caption', f'Tableau {table[\"id\"]}')}\n\n")

                # Convertir les données du tableau en Markdown
                if table.get('data'):
                    md.append(self._table_to_markdown(table['data']))
                    md.append(f"\n*Page {table.get('page')}*\n\n")

        # Annotations
        if include_annotations and annotations:
            md.append("## Annotations\n\n")

            for annotation in annotations:
                md.append(f"### {annotation.get('annotation_type', 'Note').title()} - Page {annotation.get('page')}\n\n")
                md.append(f"{annotation.get('content')}\n\n")
                md.append(f"*{annotation.get('created_at')}*\n\n")

        # Pied de page
        md.append("\n---\n\n")
        md.append(f"*Exporté le {datetime.now().strftime('%Y-%m-%d %H:%M')} depuis PDF Explorer*\n")

        return ''.join(md)

    def export_to_latex(self, document: Dict) -> str:
        """
        Exporte un document en format LaTeX.

        Args:
            document: Document à exporter

        Returns:
            Contenu LaTeX
        """
        latex = []

        # Préambule
        latex.append("\\documentclass[12pt,a4paper]{article}\n")
        latex.append("\\usepackage[utf8]{inputenc}\n")
        latex.append("\\usepackage[french]{babel}\n")
        latex.append("\\usepackage{graphicx}\n")
        latex.append("\\usepackage{hyperref}\n")
        latex.append("\\usepackage{booktabs}\n\n")

        # Titre et auteurs
        metadata = document.get('metadata', {})

        latex.append(f"\\title{{{self._escape_latex(metadata.get('title', document['filename']))}}}\n")

        if metadata.get('authors'):
            latex.append(f"\\author{{{self._escape_latex(', '.join(metadata['authors']))}}}\n")

        if metadata.get('year'):
            latex.append(f"\\date{{{metadata['year']}}}\n")

        latex.append("\n\\begin{document}\n\n")
        latex.append("\\maketitle\n\n")

        # Abstract
        if metadata.get('abstract'):
            latex.append("\\begin{abstract}\n")
            latex.append(f"{self._escape_latex(metadata['abstract'])}\n")
            latex.append("\\end{abstract}\n\n")

        # Sections
        sections = document.get('sections', [])

        for section in sections:
            section_command = "\\section" if section.get('level', 1) == 1 else "\\subsection"
            latex.append(f"{section_command}{{{self._escape_latex(section['title'])}}}\n\n")
            latex.append(f"{self._escape_latex(section['content'])}\n\n")

        latex.append("\\end{document}\n")

        return ''.join(latex)

    def export_to_json(self, document: Dict, include_annotations: bool = True, annotations: List[Dict] = None) -> str:
        """
        Exporte un document en format JSON.

        Args:
            document: Document à exporter
            include_annotations: Inclure les annotations
            annotations: Liste d'annotations

        Returns:
            Contenu JSON
        """
        export_data = {
            'metadata': document.get('metadata', {}),
            'document_info': {
                'id': document.get('id'),
                'filename': document.get('filename'),
                'num_pages': document.get('num_pages'),
                'file_size': document.get('file_size'),
                'indexed_at': str(document.get('indexed_at'))
            },
            'sections': document.get('sections', []),
            'figures': document.get('figures', []),
            'tables': document.get('tables', []),
            'full_text': document.get('full_text', ''),
            'export_info': {
                'exported_at': datetime.now().isoformat(),
                'exported_from': 'PDF Explorer'
            }
        }

        if include_annotations and annotations:
            export_data['annotations'] = annotations

        return json.dumps(export_data, ensure_ascii=False, indent=2, default=str)

    def export_summary_to_pdf_html(self, document: Dict) -> str:
        """
        Génère un HTML qui peut être converti en PDF (fiche de synthèse).

        Args:
            document: Document

        Returns:
            HTML de la fiche de synthèse
        """
        html = []

        html.append("<!DOCTYPE html>\n")
        html.append("<html lang='fr'>\n")
        html.append("<head>\n")
        html.append("<meta charset='UTF-8'>\n")
        html.append("<title>Fiche de Synthèse</title>\n")
        html.append("<style>\n")
        html.append("""
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
            h1 { color: #2563eb; border-bottom: 3px solid #2563eb; padding-bottom: 10px; }
            h2 { color: #1e40af; margin-top: 30px; }
            .metadata { background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0; }
            .metadata p { margin: 5px 0; }
            .stat-box { display: inline-block; background: #dbeafe; padding: 15px 20px; margin: 10px; border-radius: 8px; text-align: center; }
            .stat-box .number { font-size: 32px; font-weight: bold; color: #2563eb; }
            .stat-box .label { font-size: 14px; color: #1e40af; }
            .section-preview { background: #f9fafb; padding: 10px; margin: 10px 0; border-left: 4px solid #3b82f6; }
        """)
        html.append("</style>\n")
        html.append("</head>\n")
        html.append("<body>\n")

        # Titre
        title = document.get('metadata', {}).get('title', document['filename'])
        html.append(f"<h1>{self._escape_html(title)}</h1>\n")

        # Métadonnées
        metadata = document.get('metadata', {})
        html.append("<div class='metadata'>\n")

        if metadata.get('authors'):
            html.append(f"<p><strong>Auteurs:</strong> {self._escape_html(', '.join(metadata['authors']))}</p>\n")

        if metadata.get('year'):
            html.append(f"<p><strong>Année:</strong> {metadata['year']}</p>\n")

        if metadata.get('keywords'):
            html.append(f"<p><strong>Mots-clés:</strong> {self._escape_html(', '.join(metadata['keywords']))}</p>\n")

        html.append("</div>\n")

        # Statistiques
        html.append("<h2>Statistiques</h2>\n")
        html.append("<div class='stat-box'>\n")
        html.append(f"<div class='number'>{document.get('num_pages', 0)}</div>\n")
        html.append("<div class='label'>Pages</div>\n")
        html.append("</div>\n")

        html.append("<div class='stat-box'>\n")
        html.append(f"<div class='number'>{len(document.get('sections', []))}</div>\n")
        html.append("<div class='label'>Sections</div>\n")
        html.append("</div>\n")

        html.append("<div class='stat-box'>\n")
        html.append(f"<div class='number'>{len(document.get('figures', []))}</div>\n")
        html.append("<div class='label'>Figures</div>\n")
        html.append("</div>\n")

        html.append("<div class='stat-box'>\n")
        html.append(f"<div class='number'>{len(document.get('tables', []))}</div>\n")
        html.append("<div class='label'>Tableaux</div>\n")
        html.append("</div>\n")

        # Résumé
        if metadata.get('abstract'):
            html.append("<h2>Résumé</h2>\n")
            html.append(f"<p>{self._escape_html(metadata['abstract'])}</p>\n")

        # Sections principales
        sections = document.get('sections', [])[:5]  # Top 5
        if sections:
            html.append("<h2>Sections Principales</h2>\n")

            for section in sections:
                html.append("<div class='section-preview'>\n")
                html.append(f"<h3>{self._escape_html(section['title'])}</h3>\n")

                preview = section['content'][:200] + "..." if len(section['content']) > 200 else section['content']
                html.append(f"<p>{self._escape_html(preview)}</p>\n")
                html.append("</div>\n")

        # Pied de page
        html.append(f"<p style='margin-top: 40px; text-align: center; color: #6b7280; font-size: 12px;'>")
        html.append(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} par PDF Explorer</p>\n")

        html.append("</body>\n")
        html.append("</html>\n")

        return ''.join(html)

    def export_citations(self, references: List[Dict], format: str = 'bibtex') -> str:
        """
        Exporte les références bibliographiques.

        Args:
            references: Liste de références
            format: Format d'export (bibtex, ris, endnote)

        Returns:
            Références formatées
        """
        if format == 'bibtex':
            return self._export_bibtex(references)
        elif format == 'ris':
            return self._export_ris(references)
        else:
            return json.dumps(references, ensure_ascii=False, indent=2)

    def _export_bibtex(self, references: List[Dict]) -> str:
        """Exporte en format BibTeX."""
        entries = []

        for ref in references:
            entry_id = f"ref{ref.get('number', '')}"
            entry = f"@article{{{entry_id},\n"

            if ref.get('authors'):
                entry += f"  author = {{{ref['authors']}}},\n"

            if ref.get('title'):
                entry += f"  title = {{{ref['title']}}},\n"

            if ref.get('journal'):
                entry += f"  journal = {{{ref['journal']}}},\n"

            if ref.get('year'):
                entry += f"  year = {{{ref['year']}}},\n"

            if ref.get('doi'):
                entry += f"  doi = {{{ref['doi']}}},\n"

            entry += "}\n"
            entries.append(entry)

        return '\n'.join(entries)

    def _export_ris(self, references: List[Dict]) -> str:
        """Exporte en format RIS."""
        entries = []

        for ref in references:
            entry = ["TY  - JOUR"]  # Journal Article

            if ref.get('authors'):
                entry.append(f"AU  - {ref['authors']}")

            if ref.get('title'):
                entry.append(f"TI  - {ref['title']}")

            if ref.get('journal'):
                entry.append(f"JO  - {ref['journal']}")

            if ref.get('year'):
                entry.append(f"PY  - {ref['year']}")

            if ref.get('doi'):
                entry.append(f"DO  - {ref['doi']}")

            entry.append("ER  -\n")
            entries.append('\n'.join(entry))

        return '\n'.join(entries)

    def _table_to_markdown(self, table_data: List[List[str]]) -> str:
        """Convertit un tableau en Markdown."""
        if not table_data:
            return ""

        md = []

        # En-tête
        header = table_data[0]
        md.append("| " + " | ".join(str(cell) for cell in header) + " |")
        md.append("| " + " | ".join("---" for _ in header) + " |")

        # Lignes
        for row in table_data[1:]:
            md.append("| " + " | ".join(str(cell) for cell in row) + " |")

        return "\n".join(md) + "\n"

    def _escape_latex(self, text: str) -> str:
        """Échappe les caractères spéciaux LaTeX."""
        special_chars = {
            '&': '\\&',
            '%': '\\%',
            '$': '\\$',
            '#': '\\#',
            '_': '\\_',
            '{': '\\{',
            '}': '\\}',
            '~': '\\textasciitilde{}',
            '^': '\\^{}',
            '\\': '\\textbackslash{}'
        }

        for char, escaped in special_chars.items():
            text = text.replace(char, escaped)

        return text

    def _escape_html(self, text: str) -> str:
        """Échappe les caractères spéciaux HTML."""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))
