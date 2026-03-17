import React from 'react';
import { Navbar } from '../components/Layout/Navbar';
import { Sidebar } from '../components/Layout/Sidebar';

export const HourLogsPage = () => {
  return (
    <div className="app-main">
      <Navbar />
      <div className="main-layout">
        <Sidebar activeRoute="/hours" />
        <main className="main-content">
          <div className="page-header">
            <h1 className="page-title">Hour Logs</h1>
            <p className="page-subtitle">View your submitted hours</p>
          </div>
          <div className="card">
            <p>Hour logs component coming soon...</p>
          </div>
        </main>
      </div>
    </div>
  );
};
