import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Navbar } from '../components/Layout/Navbar';
import { Sidebar } from '../components/Layout/Sidebar';

export const ApprenticeDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  return (
    <div className="app-main">
      <Navbar />
      <div className="main-layout">
        <Sidebar activeRoute="/apprentices" />
        <main className="main-content">
          <div className="page-header">
            <div className="page-header-left">
              <h1 className="page-title">Apprentice Details</h1>
            </div>
            <div className="page-actions">
              <button className="btn btn-secondary" onClick={() => navigate(-1)}>
                ← Back
              </button>
            </div>
          </div>
          <div className="card">
            <p>Loading apprentice {id}...</p>
          </div>
        </main>
      </div>
    </div>
  );
};
