import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import DocumentList from './pages/DocumentList';
import DocumentViewer from './pages/DocumentViewer';
import Search from './pages/Search';
import Interactive from './pages/Interactive';
import Advanced from './pages/Advanced';
import Learning from './pages/Learning';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/documents" element={<DocumentList />} />
          <Route path="/documents/:documentId" element={<DocumentViewer />} />
          <Route path="/search" element={<Search />} />
          <Route path="/interactive/:documentId" element={<Interactive />} />
          <Route path="/advanced/:documentId" element={<Advanced />} />
          <Route path="/learning/:documentId" element={<Learning />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
