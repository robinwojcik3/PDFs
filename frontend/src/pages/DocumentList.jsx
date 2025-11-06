import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FileText, Users, Calendar, Image, Table2, Sparkles } from 'lucide-react';
import { documentsAPI } from '../services/api';

export default function DocumentList() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await documentsAPI.list();
      setDocuments(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Erreur lors du chargement des documents");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card bg-red-50 border border-red-200">
        <p className="text-red-900">{error}</p>
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="card text-center space-y-4">
        <FileText className="w-16 h-16 mx-auto text-gray-400" />
        <h2 className="text-2xl font-semibold text-gray-700">Aucun document indexé</h2>
        <p className="text-gray-600">
          Placez vos PDFs dans le dossier <code className="bg-gray-100 px-2 py-1 rounded">data/pdfs/</code>
          et indexez-les depuis la page d'accueil.
        </p>
        <Link to="/" className="btn-primary inline-block">
          Retour à l'accueil
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Documents indexés</h1>
        <div className="text-sm text-gray-600">
          {documents.length} document{documents.length > 1 ? 's' : ''}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {documents.map((doc) => (
          <div key={doc.id} className="card hover:shadow-lg transition-shadow duration-200">
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                  <FileText className="w-6 h-6 text-primary-600" />
                </div>
              </div>

              <div className="flex-1 min-w-0">
                <Link
                  to={`/documents/${doc.id}`}
                  className="text-xl font-semibold text-gray-900 hover:text-primary-600 transition-colors"
                >
                  {doc.title || doc.filename}
                </Link>

                <div className="mt-2 flex flex-wrap items-center gap-4 text-sm text-gray-600">
                  {doc.authors && doc.authors.length > 0 && (
                    <div className="flex items-center space-x-1">
                      <Users className="w-4 h-4" />
                      <span>{doc.authors.join(', ')}</span>
                    </div>
                  )}

                  {doc.year && (
                    <div className="flex items-center space-x-1">
                      <Calendar className="w-4 h-4" />
                      <span>{doc.year}</span>
                    </div>
                  )}

                  <div className="flex items-center space-x-1">
                    <FileText className="w-4 h-4" />
                    <span>{doc.num_pages} page{doc.num_pages > 1 ? 's' : ''}</span>
                  </div>

                  {doc.num_figures > 0 && (
                    <div className="flex items-center space-x-1">
                      <Image className="w-4 h-4" />
                      <span>{doc.num_figures} figure{doc.num_figures > 1 ? 's' : ''}</span>
                    </div>
                  )}

                  {doc.num_tables > 0 && (
                    <div className="flex items-center space-x-1">
                      <Table2 className="w-4 h-4" />
                      <span>{doc.num_tables} tableau{doc.num_tables > 1 ? 'x' : ''}</span>
                    </div>
                  )}
                </div>

                <div className="mt-4 flex items-center space-x-3">
                  <Link
                    to={`/documents/${doc.id}`}
                    className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                  >
                    Voir le document →
                  </Link>

                  <Link
                    to={`/interactive/${doc.id}`}
                    className="text-sm text-purple-600 hover:text-purple-700 font-medium flex items-center space-x-1"
                  >
                    <Sparkles className="w-4 h-4" />
                    <span>Modules interactifs</span>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
