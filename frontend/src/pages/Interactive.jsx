import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ChevronLeft,
  Brain,
  BarChart3,
  FileText,
  CheckCircle,
  XCircle,
} from 'lucide-react';
import { interactiveAPI, documentsAPI } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function Interactive() {
  const { documentId } = useParams();
  const [document, setDocument] = useState(null);
  const [concepts, setConcepts] = useState(null);
  const [quiz, setQuiz] = useState(null);
  const [summary, setSummary] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('concepts');
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);

  useEffect(() => {
    loadData();
  }, [documentId]);

  const loadData = async () => {
    try {
      const [docRes, conceptsRes, quizRes, summaryRes, statsRes] = await Promise.all([
        documentsAPI.get(documentId),
        interactiveAPI.getConcepts(documentId),
        interactiveAPI.getQuiz(documentId),
        interactiveAPI.getSummary(documentId),
        interactiveAPI.getStatistics(documentId),
      ]);

      setDocument(docRes.data);
      setConcepts(conceptsRes.data);
      setQuiz(quizRes.data);
      setSummary(summaryRes.data);
      setStatistics(statsRes.data);
    } catch (error) {
      console.error('Erreur chargement:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleQuizAnswer = (questionId, answerIndex) => {
    setQuizAnswers({ ...quizAnswers, [questionId]: answerIndex });
  };

  const handleQuizSubmit = () => {
    setQuizSubmitted(true);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const tabs = [
    { id: 'concepts', label: 'Concepts Clés', icon: Brain },
    { id: 'quiz', label: 'Quiz Pédagogique', icon: CheckCircle },
    { id: 'summary', label: 'Fiche de Synthèse', icon: FileText },
    { id: 'statistics', label: 'Statistiques', icon: BarChart3 },
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
            Modules Pédagogiques Interactifs
          </h1>
          <p className="text-gray-600">
            {document?.metadata?.title || document?.filename}
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
                    ? 'border-purple-600 text-purple-600'
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
        {activeTab === 'concepts' && concepts && (
          <div className="space-y-6">
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Concepts Clés Extraits</h2>
              <p className="text-gray-600 mb-6">
                Les termes les plus fréquents et importants du document.
              </p>

              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {concepts.concepts.map((concept, idx) => (
                  <div
                    key={idx}
                    className="bg-gradient-to-br from-purple-50 to-blue-50 p-4 rounded-lg border border-purple-200"
                  >
                    <div className="font-semibold text-gray-900 mb-2">
                      {concept.term}
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="flex-1 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-purple-600 h-2 rounded-full"
                          style={{ width: `${concept.importance}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-gray-600">
                        {concept.frequency}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {concepts.keywords && concepts.keywords.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold mb-3">Mots-clés du document</h3>
                <div className="flex flex-wrap gap-2">
                  {concepts.keywords.map((keyword, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'quiz' && quiz && (
          <div className="card">
            <h2 className="text-xl font-semibold mb-2">{quiz.quiz_title}</h2>
            <p className="text-gray-600 mb-6">
              {quiz.total_questions} question{quiz.total_questions > 1 ? 's' : ''}
            </p>

            <div className="space-y-6">
              {quiz.questions.map((question, qIdx) => {
                const userAnswer = quizAnswers[question.id];
                const isCorrect =
                  quizSubmitted &&
                  userAnswer !== undefined &&
                  userAnswer === question.correct_answer;
                const isIncorrect =
                  quizSubmitted &&
                  userAnswer !== undefined &&
                  userAnswer !== question.correct_answer;

                return (
                  <div
                    key={question.id}
                    className={`p-4 rounded-lg border-2 ${
                      quizSubmitted
                        ? isCorrect
                          ? 'border-green-300 bg-green-50'
                          : isIncorrect
                          ? 'border-red-300 bg-red-50'
                          : 'border-gray-200'
                        : 'border-gray-200'
                    }`}
                  >
                    <div className="flex items-start space-x-3 mb-4">
                      <span className="flex-shrink-0 w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                        {qIdx + 1}
                      </span>
                      <p className="flex-1 font-medium text-gray-900">
                        {question.question}
                      </p>
                    </div>

                    {question.type === 'multiple_choice' && (
                      <div className="space-y-2 ml-9">
                        {question.options.map((option, optIdx) => (
                          <label
                            key={optIdx}
                            className={`block p-3 rounded-lg border cursor-pointer transition-colors ${
                              userAnswer === optIdx
                                ? 'border-purple-600 bg-purple-50'
                                : 'border-gray-200 hover:border-purple-300'
                            } ${
                              quizSubmitted && optIdx === question.correct_answer
                                ? 'border-green-500 bg-green-50'
                                : ''
                            }`}
                          >
                            <input
                              type="radio"
                              name={question.id}
                              checked={userAnswer === optIdx}
                              onChange={() => handleQuizAnswer(question.id, optIdx)}
                              disabled={quizSubmitted}
                              className="mr-2"
                            />
                            {option}
                          </label>
                        ))}
                      </div>
                    )}

                    {quizSubmitted && question.explanation && (
                      <div className="mt-4 ml-9 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                        <p className="text-sm text-blue-900">
                          <strong>Explication :</strong> {question.explanation}
                        </p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {!quizSubmitted ? (
              <button
                onClick={handleQuizSubmit}
                disabled={Object.keys(quizAnswers).length === 0}
                className="btn-primary mt-6 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Soumettre les réponses
              </button>
            ) : (
              <div className="mt-6 p-4 bg-primary-50 border border-primary-200 rounded-lg">
                <p className="text-primary-900 font-medium">
                  Score :{' '}
                  {
                    quiz.questions.filter(
                      (q) => quizAnswers[q.id] === q.correct_answer
                    ).length
                  }{' '}
                  / {quiz.questions.length}
                </p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'summary' && summary && (
          <div className="card">
            <h2 className="text-2xl font-bold mb-6">{summary.title}</h2>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  {summary.num_pages}
                </div>
                <div className="text-sm text-gray-600">Pages</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  {summary.structure.sections}
                </div>
                <div className="text-sm text-gray-600">Sections</div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">
                  {summary.structure.figures}
                </div>
                <div className="text-sm text-gray-600">Figures</div>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-orange-600">
                  {summary.structure.tables}
                </div>
                <div className="text-sm text-gray-600">Tableaux</div>
              </div>
            </div>

            {summary.authors && summary.authors.length > 0 && (
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-2">Auteurs</h3>
                <p className="text-gray-700">
                  {summary.authors.join(', ')}
                  {summary.year && ` (${summary.year})`}
                </p>
              </div>
            )}

            {summary.abstract && (
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-2">Résumé</h3>
                <p className="text-gray-700">{summary.abstract}</p>
              </div>
            )}

            {summary.main_sections && summary.main_sections.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">
                  Sections Principales
                </h3>
                <div className="space-y-3">
                  {summary.main_sections.map((section, idx) => (
                    <div key={idx} className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900 mb-1">
                        {section.title}
                      </h4>
                      <p className="text-sm text-gray-600">{section.preview}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'statistics' && statistics && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="card bg-gradient-to-br from-blue-50 to-blue-100">
                <div className="text-3xl font-bold text-blue-600 mb-2">
                  {statistics.total_words.toLocaleString()}
                </div>
                <div className="text-sm text-gray-700">Mots au total</div>
              </div>

              <div className="card bg-gradient-to-br from-green-50 to-green-100">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {Math.round(statistics.avg_words_per_page)}
                </div>
                <div className="text-sm text-gray-700">Mots par page (moyenne)</div>
              </div>

              <div className="card bg-gradient-to-br from-purple-50 to-purple-100">
                <div className="text-3xl font-bold text-purple-600 mb-2">
                  {statistics.visual_elements.figures + statistics.visual_elements.tables}
                </div>
                <div className="text-sm text-gray-700">Éléments visuels</div>
              </div>
            </div>

            {statistics.sections_distribution && statistics.sections_distribution.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold mb-4">
                  Distribution des mots par section
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={statistics.sections_distribution}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="section"
                      angle={-45}
                      textAnchor="end"
                      height={100}
                      fontSize={12}
                    />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="word_count" fill="#3b82f6" name="Nombre de mots" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
