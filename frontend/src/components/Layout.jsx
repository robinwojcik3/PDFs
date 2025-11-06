import { Link, useLocation } from 'react-router-dom';
import { BookOpen, Search, Home, FileText, Sparkles } from 'lucide-react';

export default function Layout({ children }) {
  const location = useLocation();

  const navigation = [
    { name: 'Accueil', path: '/', icon: Home },
    { name: 'Documents', path: '/documents', icon: FileText },
    { name: 'Recherche', path: '/search', icon: Search },
  ];

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-primary-700 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <BookOpen className="w-8 h-8" />
              <div>
                <h1 className="text-xl font-bold">PDF Explorer</h1>
                <p className="text-xs text-primary-200">
                  Exploration Interactive de PDFs Scientifiques
                </p>
              </div>
            </div>

            <nav className="flex space-x-4">
              {navigation.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive(item.path)
                        ? 'bg-primary-800 text-white'
                        : 'text-primary-100 hover:bg-primary-600'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <p className="text-sm">
              © 2024 PDF Explorer - Application d'indexation interactive de PDFs scientifiques
            </p>
            <div className="flex items-center space-x-2">
              <Sparkles className="w-4 h-4" />
              <span className="text-sm">Propulsé par FastAPI & React</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
