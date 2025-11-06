import { useState } from 'react';
import { Plus, Trash2, Edit2, Save, X } from 'lucide-react';
import { annotationsAPI } from '../services/api';

export default function AnnotationPanel({
  documentId,
  annotations,
  onAnnotationCreated,
  onAnnotationsChange,
}) {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    page: 1,
    content: '',
    annotation_type: 'note',
    color: '#FFFF00',
  });

  const handleCreate = async () => {
    try {
      const response = await annotationsAPI.create({
        document_id: documentId,
        ...formData,
      });

      onAnnotationCreated(response.data);
      setShowCreateForm(false);
      setFormData({
        page: 1,
        content: '',
        annotation_type: 'note',
        color: '#FFFF00',
      });
    } catch (error) {
      console.error('Erreur création annotation:', error);
    }
  };

  const handleUpdate = async (annotationId, updates) => {
    try {
      const response = await annotationsAPI.update(documentId, annotationId, updates);
      const updatedAnnotations = annotations.map((a) =>
        a.id === annotationId ? response.data : a
      );
      onAnnotationsChange(updatedAnnotations);
      setEditingId(null);
    } catch (error) {
      console.error('Erreur mise à jour annotation:', error);
    }
  };

  const handleDelete = async (annotationId) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette annotation ?')) return;

    try {
      await annotationsAPI.delete(documentId, annotationId);
      const updatedAnnotations = annotations.filter((a) => a.id !== annotationId);
      onAnnotationsChange(updatedAnnotations);
    } catch (error) {
      console.error('Erreur suppression annotation:', error);
    }
  };

  const handleExport = async () => {
    try {
      const response = await annotationsAPI.export(documentId);
      const dataStr = JSON.stringify(response.data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `annotations-${documentId}.json`;
      link.click();
    } catch (error) {
      console.error('Erreur export annotations:', error);
    }
  };

  const annotationTypes = [
    { value: 'note', label: 'Note', color: '#FFFF00' },
    { value: 'highlight', label: 'Surlignage', color: '#FFD700' },
    { value: 'comment', label: 'Commentaire', color: '#87CEEB' },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Annotations</h3>
        <div className="flex items-center space-x-2">
          {annotations.length > 0 && (
            <button
              onClick={handleExport}
              className="btn-secondary text-sm"
            >
              Exporter
            </button>
          )}
          <button
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="btn-primary flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Nouvelle annotation</span>
          </button>
        </div>
      </div>

      {/* Create Form */}
      {showCreateForm && (
        <div className="card bg-blue-50 border border-blue-200">
          <h4 className="font-medium mb-3">Créer une annotation</h4>

          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type
              </label>
              <select
                value={formData.annotation_type}
                onChange={(e) => {
                  const type = annotationTypes.find((t) => t.value === e.target.value);
                  setFormData({
                    ...formData,
                    annotation_type: e.target.value,
                    color: type?.color || formData.color,
                  });
                }}
                className="input"
              >
                {annotationTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Page
              </label>
              <input
                type="number"
                min="1"
                value={formData.page}
                onChange={(e) =>
                  setFormData({ ...formData, page: parseInt(e.target.value) })
                }
                className="input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Contenu
              </label>
              <textarea
                value={formData.content}
                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                rows="3"
                className="input"
                placeholder="Votre annotation..."
              />
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={handleCreate}
                disabled={!formData.content.trim()}
                className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Save className="w-4 h-4 mr-2 inline" />
                Enregistrer
              </button>
              <button onClick={() => setShowCreateForm(false)} className="btn-secondary">
                <X className="w-4 h-4 mr-2 inline" />
                Annuler
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Annotations List */}
      {annotations.length === 0 ? (
        <div className="card text-center text-gray-500">
          Aucune annotation pour ce document.
          <br />
          Cliquez sur "Nouvelle annotation" pour en créer une.
        </div>
      ) : (
        <div className="space-y-3">
          {annotations.map((annotation) => {
            const isEditing = editingId === annotation.id;
            const [editContent, setEditContent] = useState(annotation.content);

            return (
              <div
                key={annotation.id}
                className="card"
                style={{ borderLeftWidth: '4px', borderLeftColor: annotation.color }}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-xs font-medium text-gray-500 uppercase">
                        {annotation.annotation_type}
                      </span>
                      <span className="text-xs text-gray-400">•</span>
                      <span className="text-xs text-gray-500">Page {annotation.page}</span>
                    </div>

                    {isEditing ? (
                      <div className="space-y-2">
                        <textarea
                          value={editContent}
                          onChange={(e) => setEditContent(e.target.value)}
                          rows="3"
                          className="input"
                        />
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => {
                              handleUpdate(annotation.id, { content: editContent });
                            }}
                            className="text-sm px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                          >
                            <Save className="w-3 h-3 inline mr-1" />
                            Enregistrer
                          </button>
                          <button
                            onClick={() => setEditingId(null)}
                            className="text-sm px-3 py-1 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                          >
                            Annuler
                          </button>
                        </div>
                      </div>
                    ) : (
                      <p className="text-gray-700 whitespace-pre-wrap">
                        {annotation.content}
                      </p>
                    )}

                    <p className="text-xs text-gray-400 mt-2">
                      {new Date(annotation.created_at).toLocaleString('fr-FR')}
                    </p>
                  </div>

                  {!isEditing && (
                    <div className="flex items-center space-x-1 ml-3">
                      <button
                        onClick={() => setEditingId(annotation.id)}
                        className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded"
                        title="Modifier"
                      >
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(annotation.id)}
                        className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded"
                        title="Supprimer"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
