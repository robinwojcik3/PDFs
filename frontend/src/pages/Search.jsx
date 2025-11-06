import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Search as SearchIcon, FileText, Sparkles } from 'lucide-react';
import { searchAPI } from '../services/api';

export default function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!query.trim()) return;

    setLoading(true);
    setSearched(true);

    try {
      const response = await searchAPI.search(query);
      setResults(response.data);
    } catch (error) {
      console.error('Erreur de recherche:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="card">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Recherche dans les documents
        </h1>

        <form onSubmit={handleSearch} className="flex space-x-3">
          <div className="flex-1 relative">
            <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Rechercher dans tous les documents..."
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed px-8"
          >
            {loading ? 'Recherche...' : 'Rechercher'}
          </button>
        </form>

        <div className="mt-4 flex flex-wrap gap-2">
          <span className="text-sm text-gray-600">Exemples :</span>
          {['algorithme', 'résultats', 'méthode', 'conclusion'].map((example) => (
            <button
              key={example}
              onClick={() => setQuery(example)}
              className="text-sm px-3 py-1 bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      {searched && (
        <div>
          {loading ? (
            <div className="flex items-center justify-center h-32">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            </div>
          ) : results.length > 0 ? (
            <div className="space-y-4">
              <p className="text-gray-600">
                {results.length} résultat{results.length > 1 ? 's' : ''} trouvé
                {results.length > 1 ? 's' : ''} pour "{query}"
              </p>

              {results.map((result, idx) => (
                <div key={idx} className="card hover:shadow-lg transition-shadow duration-200">
                  <div className="flex items-start space-x-3">
                    <FileText className="w-5 h-5 text-primary-600 flex-shrink-0 mt-1" />

                    <div className="flex-1 min-w-0">
                      <Link
                        to={`/documents/${result.document_id}`}
                        className="text-lg font-semibold text-primary-600 hover:text-primary-700"
                      >
                        {result.title}
                      </Link>

                      <p className="text-sm text-gray-500 mb-2">{result.filename}</p>

                      <div className="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg">
                        <p dangerouslySetInnerHTML={{ __html: result.snippet }}></p>
                      </div>

                      <div className="mt-3 flex items-center space-x-4 text-sm">
                        <span className="text-gray-500">
                          Score: {result.score.toFixed(2)}
                        </span>
                        {result.page && (
                          <>
                            <span className="text-gray-400">•</span>
                            <span className="text-gray-500">Page {result.page}</span>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="card text-center space-y-3">
              <SearchIcon className="w-12 h-12 mx-auto text-gray-400" />
              <h3 className="text-lg font-medium text-gray-900">
                Aucun résultat trouvé
              </h3>
              <p className="text-gray-600">
                Essayez avec d'autres mots-clés ou termes de recherche.
              </p>
            </div>
          )}
        </div>
      )}

      {!searched && (
        <div className="card text-center space-y-4">
          <Sparkles className="w-16 h-16 mx-auto text-primary-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            Recherche full-text
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Recherchez dans tout le contenu de vos documents indexés : titres, textes complets,
            sections, abstracts et mots-clés. Les résultats sont triés par pertinence.
          </p>
        </div>
      )}
    </div>
  );
}
