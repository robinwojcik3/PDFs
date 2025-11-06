/**
 * Page des applications pédagogiques interactives basées sur les concepts scientifiques.
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  BookOpen, BarChart3, Beaker, GitBranch, Calculator,
  Clock, ImageIcon, ArrowLeftRight, AlertCircle, Loader2,
  Lightbulb, Brain, Target, TrendingUp
} from 'lucide-react';
import { learningAPI, documentsAPI } from '../services/api';

const Learning = () => {
  const { documentId } = useParams();
  const navigate = useNavigate();

  const [document, setDocument] = useState(null);
  const [interactions, setInteractions] = useState(null);
  const [selectedType, setSelectedType] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, [documentId]);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Charger le document
      const docResponse = await documentsAPI.get(documentId);
      setDocument(docResponse.data);

      // Charger toutes les interactions
      const interactionsResponse = await learningAPI.getAllInteractions(documentId, true);
      setInteractions(interactionsResponse.data);

    } catch (err) {
      console.error('Erreur lors du chargement:', err);
      setError(err.response?.data?.detail || 'Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  const getTypeIcon = (type) => {
    const icons = {
      visualization: BarChart3,
      simulation: Beaker,
      diagram: GitBranch,
      exercise: Target,
      calculator: Calculator,
      timeline: Clock,
      graph_explorer: ImageIcon,
      comparison: ArrowLeftRight
    };
    return icons[type] || Lightbulb;
  };

  const getTypeColor = (type) => {
    const colors = {
      visualization: 'text-blue-600 bg-blue-50',
      simulation: 'text-green-600 bg-green-50',
      diagram: 'text-purple-600 bg-purple-50',
      exercise: 'text-orange-600 bg-orange-50',
      calculator: 'text-indigo-600 bg-indigo-50',
      timeline: 'text-pink-600 bg-pink-50',
      graph_explorer: 'text-teal-600 bg-teal-50',
      comparison: 'text-amber-600 bg-amber-50'
    };
    return colors[type] || 'text-gray-600 bg-gray-50';
  };

  const getTypeLabel = (type) => {
    const labels = {
      visualization: 'Visualisation',
      simulation: 'Simulation',
      diagram: 'Diagramme',
      exercise: 'Exercice',
      calculator: 'Calculateur',
      timeline: 'Timeline',
      graph_explorer: 'Explorateur',
      comparison: 'Comparaison'
    };
    return labels[type] || type;
  };

  const filteredInteractions = () => {
    if (!interactions || !interactions.interactions) return [];
    if (selectedType === 'all') return interactions.interactions;
    return interactions.interactions.filter(i => i.type === selectedType);
  };

  const getTypeCounts = () => {
    if (!interactions || !interactions.interactions) return {};
    const counts = {};
    interactions.interactions.forEach(i => {
      counts[i.type] = (counts[i.type] || 0) + 1;
    });
    return counts;
  };

  const renderInteractionCard = (interaction) => {
    const Icon = getTypeIcon(interaction.type);
    const colorClass = getTypeColor(interaction.type);

    return (
      <div key={interaction.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
        <div className="flex items-start gap-4">
          <div className={`p-3 rounded-lg ${colorClass}`}>
            <Icon className="w-6 h-6" />
          </div>

          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="text-lg font-semibold text-gray-900">{interaction.title}</h3>
              <span className={`px-2 py-1 text-xs font-medium rounded ${colorClass}`}>
                {getTypeLabel(interaction.type)}
              </span>
            </div>

            <p className="text-gray-600 mb-4">{interaction.description}</p>

            {/* Concept scientifique */}
            {interaction.scientific_concept && (
              <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                <div className="flex items-center gap-2 mb-2">
                  <Brain className="w-4 h-4 text-blue-600" />
                  <span className="font-medium text-blue-900">Concept scientifique</span>
                </div>
                <p className="text-sm text-blue-800">{interaction.scientific_concept}</p>
              </div>
            )}

            {/* Configuration spécifique */}
            {interaction.config && (
              <div className="space-y-2">
                {interaction.config.data_source && (
                  <div className="text-sm">
                    <span className="font-medium text-gray-700">Source: </span>
                    <span className="text-gray-600">{interaction.config.data_source}</span>
                  </div>
                )}

                {interaction.config.parameters && (
                  <div className="text-sm">
                    <span className="font-medium text-gray-700">Paramètres ajustables: </span>
                    <span className="text-gray-600">{interaction.config.parameters.join(', ')}</span>
                  </div>
                )}

                {interaction.config.difficulty && (
                  <div className="text-sm">
                    <span className="font-medium text-gray-700">Niveau: </span>
                    <span className="text-gray-600 capitalize">{interaction.config.difficulty}</span>
                  </div>
                )}

                {interaction.config.methodology_based && (
                  <div className="flex items-center gap-2 text-sm text-green-700 bg-green-50 px-3 py-1 rounded">
                    <TrendingUp className="w-4 h-4" />
                    <span>Basé sur l'analyse méthodologique</span>
                  </div>
                )}
              </div>
            )}

            {/* Bouton d'action */}
            <div className="mt-4">
              <button className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition-colors">
                Lancer l'application interactive
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-indigo-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Génération des applications interactives...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <AlertCircle className="w-6 h-6 text-red-600" />
            <h2 className="text-xl font-semibold text-red-900">Erreur</h2>
          </div>
          <p className="text-red-700">{error}</p>
          <button
            onClick={() => navigate('/documents')}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Retour aux documents
          </button>
        </div>
      </div>
    );
  }

  const typeCounts = getTypeCounts();
  const filtered = filteredInteractions();

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* En-tête */}
      <div className="mb-8">
        <button
          onClick={() => navigate(`/documents/${documentId}`)}
          className="mb-4 text-indigo-600 hover:text-indigo-800 flex items-center gap-2"
        >
          ← Retour au document
        </button>

        <div className="flex items-center gap-4 mb-4">
          <Brain className="w-10 h-10 text-indigo-600" />
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Applications Pédagogiques Interactives</h1>
            <p className="text-gray-600 mt-1">
              {document?.metadata?.title || 'Document'}
            </p>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <Lightbulb className="w-5 h-5 text-blue-600 mt-0.5" />
            <div>
              <h3 className="font-semibold text-blue-900 mb-1">Applications basées sur les concepts</h3>
              <p className="text-sm text-blue-800">
                Ces applications interactives sont conçues pour les chercheurs experts. Elles permettent d'explorer
                en profondeur les concepts scientifiques présentés dans l'article, en intégrant les nuances
                méthodologiques et les points complexes.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Statistiques */}
      {interactions && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-3xl font-bold text-indigo-600 mb-1">
              {interactions.interactions?.length || 0}
            </div>
            <div className="text-sm text-gray-600">Applications disponibles</div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-3xl font-bold text-blue-600 mb-1">
              {typeCounts.visualization || 0}
            </div>
            <div className="text-sm text-gray-600">Visualisations</div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-3xl font-bold text-green-600 mb-1">
              {typeCounts.simulation || 0}
            </div>
            <div className="text-sm text-gray-600">Simulations</div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-3xl font-bold text-purple-600 mb-1">
              {typeCounts.exercise || 0}
            </div>
            <div className="text-sm text-gray-600">Exercices</div>
          </div>
        </div>
      )}

      {/* Filtres par type */}
      <div className="mb-6">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedType('all')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              selectedType === 'all'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Tous ({interactions?.interactions?.length || 0})
          </button>

          {Object.keys(typeCounts).map(type => {
            const Icon = getTypeIcon(type);
            return (
              <button
                key={type}
                onClick={() => setSelectedType(type)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2 ${
                  selectedType === type
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <Icon className="w-4 h-4" />
                {getTypeLabel(type)} ({typeCounts[type]})
              </button>
            );
          })}
        </div>
      </div>

      {/* Liste des applications */}
      <div className="space-y-6">
        {filtered.length > 0 ? (
          filtered.map(interaction => renderInteractionCard(interaction))
        ) : (
          <div className="bg-gray-50 rounded-lg p-12 text-center">
            <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">Aucune application interactive disponible pour ce filtre.</p>
          </div>
        )}
      </div>

      {/* Note méthodologique */}
      {interactions?.methodology_analysis && (
        <div className="mt-8 bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="font-semibold text-green-900 mb-2">Analyse méthodologique intégrée</h3>
          <p className="text-sm text-green-800">
            Les applications interactives utilisent l'analyse méthodologique de l'article
            (score de rigueur: {interactions.methodology_analysis.rigor_score}/100) pour adapter
            le niveau de complexité et les exercices proposés.
          </p>
        </div>
      )}
    </div>
  );
};

export default Learning;
