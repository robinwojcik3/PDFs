import { useState } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, Search, FileText, Sparkles, Upload, CheckCircle } from 'lucide-react';
import { documentsAPI } from '../services/api';

export default function Home() {
  const [indexing, setIndexing] = useState(false);
  const [indexResult, setIndexResult] = useState(null);

  const handleIndexDocuments = async () => {
    setIndexing(true);
    setIndexResult(null);

    try {
      const response = await documentsAPI.index();
      setIndexResult({
        success: true,
        message: response.data.message,
        files: response.data.files,
      });
    } catch (error) {
      setIndexResult({
        success: false,
        message: error.response?.data?.detail || "Erreur lors de l'indexation",
      });
    } finally {
      setIndexing(false);
    }
  };

  const features = [
    {
      icon: FileText,
      title: 'Exploration de Documents',
      description: 'Parcourez tous vos PDFs scientifiques indexés avec une navigation intuitive.',
      link: '/documents',
    },
    {
      icon: Search,
      title: 'Recherche Full-Text',
      description: 'Recherchez dans tous les documents avec des résultats pertinents et surlignés.',
      link: '/search',
    },
    {
      icon: Sparkles,
      title: 'Modules Interactifs',
      description: 'Explorez les concepts clés avec des quiz, statistiques et visualisations.',
    },
    {
      icon: BookOpen,
      title: 'Annotations',
      description: "Annotez vos documents avec des notes, surlignages et commentaires personnalisés.",
    },
  ];

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold text-gray-900">
          Bienvenue sur PDF Explorer
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Une application interactive pour explorer, annoter et enseigner les concepts
          scientifiques à partir de vos articles PDF.
        </p>
      </div>

      {/* Indexation Section */}
      <div className="card max-w-2xl mx-auto">
        <div className="text-center space-y-4">
          <Upload className="w-16 h-16 mx-auto text-primary-600" />
          <h2 className="text-2xl font-semibold">Indexer vos documents</h2>
          <p className="text-gray-600">
            Placez vos fichiers PDF dans le dossier <code className="bg-gray-100 px-2 py-1 rounded">data/pdfs/</code>
            puis lancez l'indexation pour commencer à explorer.
          </p>

          <button
            onClick={handleIndexDocuments}
            disabled={indexing}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {indexing ? 'Indexation en cours...' : 'Indexer les documents'}
          </button>

          {indexResult && (
            <div
              className={`p-4 rounded-lg ${
                indexResult.success
                  ? 'bg-green-50 border border-green-200'
                  : 'bg-red-50 border border-red-200'
              }`}
            >
              <div className="flex items-start space-x-3">
                {indexResult.success && (
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                )}
                <div className="flex-1 text-left">
                  <p
                    className={`font-medium ${
                      indexResult.success ? 'text-green-900' : 'text-red-900'
                    }`}
                  >
                    {indexResult.message}
                  </p>
                  {indexResult.files && indexResult.files.length > 0 && (
                    <ul className="mt-2 space-y-1 text-sm text-green-700">
                      {indexResult.files.map((file, idx) => (
                        <li key={idx}>• {file}</li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {features.map((feature, idx) => {
          const Icon = feature.icon;
          const content = (
            <div className="card hover:shadow-lg transition-shadow duration-200 h-full">
              <div className="flex flex-col items-center text-center space-y-3">
                <div className="p-3 bg-primary-100 rounded-full">
                  <Icon className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            </div>
          );

          return feature.link ? (
            <Link key={idx} to={feature.link}>
              {content}
            </Link>
          ) : (
            <div key={idx}>{content}</div>
          );
        })}
      </div>

      {/* Quick Start Guide */}
      <div className="card bg-primary-50 border border-primary-200">
        <h2 className="text-2xl font-semibold mb-4 text-primary-900">
          Guide de démarrage rapide
        </h2>
        <ol className="space-y-3 text-gray-700">
          <li className="flex items-start space-x-3">
            <span className="flex-shrink-0 w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
              1
            </span>
            <span>
              Placez vos fichiers PDF dans le dossier <code className="bg-white px-2 py-1 rounded">data/pdfs/</code>
            </span>
          </li>
          <li className="flex items-start space-x-3">
            <span className="flex-shrink-0 w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
              2
            </span>
            <span>Cliquez sur "Indexer les documents" ci-dessus</span>
          </li>
          <li className="flex items-start space-x-3">
            <span className="flex-shrink-0 w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
              3
            </span>
            <span>
              Explorez vos documents dans la section{' '}
              <Link to="/documents" className="text-primary-600 hover:underline font-medium">
                Documents
              </Link>
            </span>
          </li>
          <li className="flex items-start space-x-3">
            <span className="flex-shrink-0 w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
              4
            </span>
            <span>Utilisez la recherche, annotez et explorez les modules interactifs</span>
          </li>
        </ol>
      </div>
    </div>
  );
}
