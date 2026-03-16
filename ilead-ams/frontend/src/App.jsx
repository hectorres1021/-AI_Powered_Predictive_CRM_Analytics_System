import React, { useState } from 'react';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';
import { Navbar } from './components/Layout/Navbar';
import { Sidebar } from './components/Layout/Sidebar';
import { DashboardStats } from './components/Dashboard/DashboardStats';
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

          <DashboardStats />

          <div className="info-box">
            <h2>Phase 7B: Component Migration Progress</h2>
            <ul>
              <li>✅ Phase 7A: Project setup & API integration</li>
              <li>✅ Phase 7B (1/5): Authentication & Navigation</li>
              <li>✅ Phase 7B (2/5): Dashboard Statistics</li>
              <li>⏳ Phase 7B (3/5): Apprentice management</li>
              <li>⏳ Phase 7B (4/5): Hour log operations</li>
              <li>⏳ Phase 7B (5/5): User administration</li>
              <li>⏳ Phase 7C: State management optimization</li>
              <li>⏳ Phase 7D: Advanced features (analytics, reports)</li>
              <li>⏳ Phase 7E: Testing & optimization</li>
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
