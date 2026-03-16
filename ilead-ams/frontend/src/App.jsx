import React, { useState } from 'react';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';
import { Navbar } from './components/Layout/Navbar';
import { Sidebar } from './components/Layout/Sidebar';
import { AuthPage } from './pages/AuthPage';
import './App.css';

function AppContent() {
  const { isAuthenticated, loading } = useAuth();
  const [currentRoute, setCurrentRoute] = useState('/dashboard');

  if (loading) {
    return (
      <div className="app-loading">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <AuthPage onAuthSuccess={() => window.location.reload()} />;
  }

  return (
    <div className="app-main">
      <Navbar />
      <div className="main-layout">
        <Sidebar activeRoute={currentRoute} />
        <main className="main-content">
          <div className="page-header">
            <div className="page-header-left">
              <h1 className="page-title">Dashboard</h1>
              <p className="page-subtitle">Welcome to I-LEAD AMS</p>
            </div>
          </div>

          <div className="info-box">
            <h2>Phase 7B: Component Migration</h2>
            <ul>
              <li>✅ API client configured with Axios</li>
              <li>✅ Auth context and hooks set up</li>
              <li>✅ All service modules created</li>
              <li>✅ Authentication components (Login, Register, PIN)</li>
              <li>✅ Navigation (Navbar, Sidebar)</li>
              <li>⏳ Dashboard component</li>
              <li>⏳ Apprentice management components</li>
              <li>⏳ Hour log submission/approval</li>
              <li>⏳ User administration</li>
              <li>⏳ Analytics & reporting</li>
            </ul>
          </div>
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
