import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  FileText,
  Image as ImageIcon,
  Table2,
  List,
  MessageSquare,
  ChevronLeft,
  Sparkles,
} from 'lucide-react';
import { documentsAPI, annotationsAPI } from '../services/api';
import AnnotationPanel from '../components/AnnotationPanel';

export default function DocumentViewer() {
  const { documentId } = useParams();
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('sections');
  const [annotations, setAnnotations] = useState([]);

  useEffect(() => {
    loadDocument();
    loadAnnotations();
  }, [documentId]);

  const loadDocument = async () => {
    try {
      const response = await documentsAPI.get(documentId);
      setDocument(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors du chargement');
    } finally {
      setLoading(false);
    }
  };

  const loadAnnotations = async () => {
    try {
      const response = await annotationsAPI.list(documentId);
      setAnnotations(response.data);
    } catch (err) {
      console.error('Erreur annotations:', err);
    }
  };

  const handleAnnotationCreated = (newAnnotation) => {
    setAnnotations([...annotations, newAnnotation]);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !document) {
    return (
      <div className="card bg-red-50 border border-red-200">
        <p className="text-red-900">{error || 'Document non trouvé'}</p>
        <Link to="/documents" className="text-primary-600 hover:underline mt-2 inline-block">
          ← Retour aux documents
        </Link>
      </div>
    );
  }

  const tabs = [
    { id: 'sections', label: 'Sections', icon: List, count: document.sections?.length },
    { id: 'figures', label: 'Figures', icon: ImageIcon, count: document.figures?.length },
    { id: 'tables', label: 'Tableaux', icon: Table2, count: document.tables?.length },
    { id: 'annotations', label: 'Annotations', icon: MessageSquare, count: annotations.length },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Link
          to="/documents"
          className="inline-flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Retour aux documents</span>
        </Link>

        <div className="card">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                {document.metadata?.title || document.filename}
              </h1>

              {document.metadata?.authors && document.metadata.authors.length > 0 && (
                <p className="text-gray-600 mb-2">
                  Par {document.metadata.authors.join(', ')}
                  {document.metadata.year && ` (${document.metadata.year})`}
                </p>
              )}

              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <span>{document.num_pages} pages</span>
                <span>•</span>
                <span>{document.figures?.length || 0} figures</span>
                <span>•</span>
                <span>{document.tables?.length || 0} tableaux</span>
              </div>

              {document.metadata?.abstract && (
                <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-semibold text-sm text-gray-700 mb-2">Résumé</h3>
                  <p className="text-sm text-gray-600">{document.metadata.abstract}</p>
                </div>
              )}
            </div>

            <Link
              to={`/interactive/${documentId}`}
              className="btn-primary flex items-center space-x-2"
            >
              <Sparkles className="w-4 h-4" />
              <span>Modules interactifs</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-primary-600 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
                {tab.count > 0 && (
                  <span
                    className={`px-2 py-0.5 rounded-full text-xs ${
                      activeTab === tab.id
                        ? 'bg-primary-100 text-primary-700'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {tab.count}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Content */}
      <div>
        {activeTab === 'sections' && (
          <div className="space-y-4">
            {document.sections && document.sections.length > 0 ? (
              document.sections.map((section, idx) => (
                <div key={idx} className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {section.title}
                  </h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{section.content}</p>
                  <p className="text-xs text-gray-500 mt-2">
                    Pages {section.page_start}-{section.page_end}
                  </p>
                </div>
              ))
            ) : (
              <div className="card text-center text-gray-500">
                Aucune section détectée dans ce document.
              </div>
            )}
          </div>
        )}

        {activeTab === 'figures' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {document.figures && document.figures.length > 0 ? (
              document.figures.map((figure) => (
                <div key={figure.id} className="card">
                  <div className="aspect-video bg-gray-100 rounded-lg mb-3 flex items-center justify-center">
                    <ImageIcon className="w-12 h-12 text-gray-400" />
                  </div>
                  <h4 className="font-medium text-gray-900">{figure.caption}</h4>
                  <p className="text-sm text-gray-500">Page {figure.page}</p>
                </div>
              ))
            ) : (
              <div className="col-span-full card text-center text-gray-500">
                Aucune figure détectée dans ce document.
              </div>
            )}
          </div>
        )}

        {activeTab === 'tables' && (
          <div className="space-y-6">
            {document.tables && document.tables.length > 0 ? (
              document.tables.map((table) => (
                <div key={table.id} className="card overflow-x-auto">
                  <h4 className="font-medium text-gray-900 mb-3">{table.caption}</h4>
                  <table className="min-w-full divide-y divide-gray-200">
                    <tbody className="bg-white divide-y divide-gray-200">
                      {table.data.map((row, rowIdx) => (
                        <tr key={rowIdx}>
                          {row.map((cell, cellIdx) => (
                            <td
                              key={cellIdx}
                              className="px-4 py-2 text-sm text-gray-900 border border-gray-200"
                            >
                              {cell || '-'}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  <p className="text-sm text-gray-500 mt-2">Page {table.page}</p>
                </div>
              ))
            ) : (
              <div className="card text-center text-gray-500">
                Aucun tableau détecté dans ce document.
              </div>
            )}
          </div>
        )}

        {activeTab === 'annotations' && (
          <AnnotationPanel
            documentId={documentId}
            annotations={annotations}
            onAnnotationCreated={handleAnnotationCreated}
            onAnnotationsChange={setAnnotations}
          />
        )}
      </div>
    </div>
  );
}
