import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ChevronLeft,
  Book,
  Calculator,
  FileCode,
  Download,
  Share2,
  TrendingUp,
} from 'lucide-react';
import { advancedAPI } from '../services/api';

export default function Advanced() {
  const { documentId } = useParams();
  const [activeTab, setActiveTab] = useState('bibliography');
  const [bibliography, setBibliography] = useState(null);
  const [equations, setEquations] = useState(null);
  const [methodology, setMethodology] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [documentId]);

  const loadData = async () => {
    try {
      setLoading(true);

      // Charger toutes les données en parallèle
      const [bibRes, eqRes, methRes, recRes] = await Promise.all([
        advancedAPI.getBibliography(documentId),
        advancedAPI.getEquations(documentId),
        advancedAPI.getMethodology(documentId),
        advancedAPI.getRecommendations(documentId, 5),
      ]);

      setBibliography(bibRes.data);
      setEquations(eqRes.data);
      setMethodology(methRes.data);
      setRecommendations(recRes.data);
    } catch (error) {
      console.error('Erreur chargement données avancées:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format) => {
    try {
      const response = await advancedAPI.exportDocument(documentId, format, true);

      // Télécharger le fichier
      const blob = new Blob([response.data.content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = response.data.filename;
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Erreur export:', error);
    }
  };

  const handleExportBibliography = async (format) => {
    try {
      const response = await advancedAPI.exportBibliography(documentId, format);

      const blob = new Blob([response.data.content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `bibliography.${format}`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Erreur export bibliographie:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const tabs = [
    { id: 'bibliography', label: 'Bibliographie', icon: Book },
    { id: 'equations', label: 'Équations', icon: Calculator },
    { id: 'methodology', label: 'Méthodologie', icon: FileCode },
    { id: 'recommendations', label: 'Recommandations', icon: TrendingUp },
    { id: 'export', label: 'Export', icon: Download },
  ];

  return (
    <div className="space-y-6">
      <div>
        <Link
          to={`/documents/${documentId}`}
          className="inline-flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Retour au document</span>
        </Link>

        <div className="card">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Analyse Avancée
          </h1>
          <p className="text-gray-600">
            Fonctionnalités d'analyse scientifique avancée
          </p>
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
                    ? 'border-emerald-600 text-emerald-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Content */}
      <div>
        {activeTab === 'bibliography' && bibliography && (
          <div className="space-y-6">
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">Références Bibliographiques</h2>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleExportBibliography('bibtex')}
                    className="btn-secondary text-sm"
                  >
                    Export BibTeX
                  </button>
                  <button
                    onClick={() => handleExportBibliography('ris')}
                    className="btn-secondary text-sm"
                  >
                    Export RIS
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">
                    {bibliography.total_citations}
                  </div>
                  <div className="text-sm text-gray-600">Citations</div>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">
                    {bibliography.total_references}
                  </div>
                  <div className="text-sm text-gray-600">Références</div>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">
                    {bibliography.statistics.total_citations > 0
                      ? (bibliography.total_references / bibliography.statistics.total_citations).toFixed(1)
                      : 0}
                  </div>
                  <div className="text-sm text-gray-600">Ratio Réf/Cit</div>
                </div>
              </div>

              <h3 className="font-semibold mb-3">Références ({bibliography.references.length})</h3>
              <div className="space-y-3">
                {bibliography.references.slice(0, 10).map((ref, idx) => (
                  <div key={idx} className="bg-gray-50 p-3 rounded-lg text-sm">
                    <div className="font-medium text-gray-900">
                      [{ref.number}] {ref.authors || 'Auteurs non spécifiés'}
                    </div>
                    {ref.year && (
                      <div className="text-gray-600">Année: {ref.year}</div>
                    )}
                    {ref.title && (
                      <div className="text-gray-700 mt-1">{ref.title}</div>
                    )}
                    {ref.doi && (
                      <div className="text-blue-600 mt-1">
                        <a href={`https://doi.org/${ref.doi}`} target="_blank" rel="noopener noreferrer">
                          DOI: {ref.doi}
                        </a>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'equations' && equations && (
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Équations Mathématiques</h2>

            <div className="grid grid-cols-4 gap-4 mb-6">
              <div className="bg-indigo-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-indigo-600">
                  {equations.total_equations}
                </div>
                <div className="text-sm text-gray-600">Équations</div>
              </div>
              <div className="bg-pink-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-pink-600">
                  {equations.statistics.with_latex}
                </div>
                <div className="text-sm text-gray-600">Format LaTeX</div>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-orange-600">
                  {Object.keys(equations.statistics.common_variables).length}
                </div>
                <div className="text-sm text-gray-600">Variables</div>
              </div>
              <div className="bg-teal-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-teal-600">
                  {Math.round(equations.statistics.average_length)}
                </div>
                <div className="text-sm text-gray-600">Long. moyenne</div>
              </div>
            </div>

            <div className="space-y-3">
              {equations.equations.slice(0, 10).map((eq, idx) => (
                <div key={idx} className="bg-gray-50 p-4 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-medium text-gray-500">
                      {eq.type.toUpperCase()}
                    </span>
                    <span className="text-xs text-gray-500">ID: {eq.id}</span>
                  </div>
                  <div className="font-mono text-sm bg-white p-3 rounded border border-gray-200">
                    {eq.content}
                  </div>
                  {eq.variables && eq.variables.length > 0 && (
                    <div className="mt-2 text-xs text-gray-600">
                      Variables: {eq.variables.join(', ')}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'methodology' && methodology && (
          <div className="space-y-6">
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Analyse Méthodologique</h2>

              {/* Score de rigueur */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg mb-6">
                <div className="text-center">
                  <div className="text-5xl font-bold text-indigo-600 mb-2">
                    {methodology.methodology_analysis.rigor_score}/100
                  </div>
                  <div className="text-lg text-gray-700">Score de Rigueur Méthodologique</div>
                </div>
              </div>

              {/* Type d'approche */}
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-3">Approche de Recherche</h3>
                <div className="bg-emerald-50 p-4 rounded-lg">
                  <div className="text-lg font-medium text-emerald-900">
                    {methodology.methodology_analysis.approach_type.main_type}
                  </div>
                  <div className="mt-2 flex flex-wrap gap-2">
                    {Object.keys(methodology.methodology_analysis.approach_type.approaches).map((key) => (
                      <span key={key} className="px-3 py-1 bg-emerald-100 text-emerald-700 rounded-full text-sm">
                        {key}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Méthodes statistiques */}
              {methodology.methodology_analysis.statistical_methods.length > 0 && (
                <div className="mb-6">
                  <h3 className="font-semibold text-gray-900 mb-3">Méthodes Statistiques</h3>
                  <div className="grid grid-cols-2 gap-2">
                    {methodology.methodology_analysis.statistical_methods.map((method, idx) => (
                      <div key={idx} className="bg-blue-50 px-3 py-2 rounded text-sm text-blue-900">
                        ✓ {method.method}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Design expérimental */}
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-3">Design Expérimental</h3>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="font-medium text-gray-900 mb-2">
                    {methodology.methodology_analysis.experimental_design.design_type}
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {Object.keys(methodology.methodology_analysis.experimental_design.features).map((feature) => (
                      <span key={feature} className="px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-xs">
                        {feature.replace('_', ' ')}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Échantillon */}
              {methodology.methodology_analysis.sample_info.size && (
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Informations sur l'Échantillon</h3>
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600">
                      N = {methodology.methodology_analysis.sample_info.size}
                    </div>
                    {methodology.methodology_analysis.sample_info.criteria.length > 0 && (
                      <div className="mt-2 text-sm text-purple-900">
                        {methodology.methodology_analysis.sample_info.criteria.join(', ')}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'recommendations' && recommendations && (
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Documents Recommandés</h2>

            <div className="space-y-4">
              {recommendations.recommendations.map((rec, idx) => (
                <Link
                  key={idx}
                  to={`/documents/${rec.document_id}`}
                  className="block bg-gray-50 p-4 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">{rec.title}</h3>
                      {rec.authors && rec.authors.length > 0 && (
                        <p className="text-sm text-gray-600 mt-1">
                          {rec.authors.join(', ')}
                          {rec.year && ` (${rec.year})`}
                        </p>
                      )}
                      <div className="mt-2 text-xs text-gray-500">
                        {rec.reasons.join(' • ')}
                      </div>
                    </div>
                    <div className="ml-4 text-right">
                      <div className="text-lg font-bold text-primary-600">
                        {(rec.similarity_score * 100).toFixed(0)}%
                      </div>
                      <div className="text-xs text-gray-500">Similarité</div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'export' && (
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Export de Document</h2>

            <p className="text-gray-600 mb-6">
              Exportez ce document dans différents formats pour réutilisation et partage.
            </p>

            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => handleExport('markdown')}
                className="p-6 border-2 border-gray-200 rounded-lg hover:border-primary-600 hover:bg-primary-50 transition-colors"
              >
                <FileCode className="w-8 h-8 mx-auto mb-2 text-gray-600" />
                <div className="font-medium">Markdown</div>
                <div className="text-sm text-gray-500 mt-1">
                  Format texte structuré
                </div>
              </button>

              <button
                onClick={() => handleExport('latex')}
                className="p-6 border-2 border-gray-200 rounded-lg hover:border-primary-600 hover:bg-primary-50 transition-colors"
              >
                <FileCode className="w-8 h-8 mx-auto mb-2 text-gray-600" />
                <div className="font-medium">LaTeX</div>
                <div className="text-sm text-gray-500 mt-1">
                  Document compilable
                </div>
              </button>

              <button
                onClick={() => handleExport('json')}
                className="p-6 border-2 border-gray-200 rounded-lg hover:border-primary-600 hover:bg-primary-50 transition-colors"
              >
                <FileCode className="w-8 h-8 mx-auto mb-2 text-gray-600" />
                <div className="font-medium">JSON</div>
                <div className="text-sm text-gray-500 mt-1">
                  Format structuré complet
                </div>
              </button>

              <button
                onClick={() => handleExport('html')}
                className="p-6 border-2 border-gray-200 rounded-lg hover:border-primary-600 hover:bg-primary-50 transition-colors"
              >
                <FileCode className="w-8 h-8 mx-auto mb-2 text-gray-600" />
                <div className="font-medium">HTML</div>
                <div className="text-sm text-gray-500 mt-1">
                  Fiche de synthèse
                </div>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
