import React from 'react';
import { Navbar } from '../components/Layout/Navbar';
import { Sidebar } from '../components/Layout/Sidebar';

export const ApprovalsPage = () => {
  return (
    <div className="app-main">
      <Navbar />
      <div className="main-layout">
        <Sidebar activeRoute="/approvals" />
        <main className="main-content">
          <div className="page-header">
            <h1 className="page-title">Hour Approvals</h1>
            <p className="page-subtitle">Review and approve submitted hours</p>
          </div>
          <div className="card">
            <p>Approvals component coming soon...</p>
          </div>
        </main>
      </div>
    </div>
  );
};
