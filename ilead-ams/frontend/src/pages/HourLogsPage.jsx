import React from 'react';
import { Navbar } from '../components/Layout/Navbar';
import { Sidebar } from '../components/Layout/Sidebar';
import { HourLogList } from '../components/HourLogs/HourLogList';

export const HourLogsPage = () => {
  return (
    <div className="app-main">
      <Navbar />
      <div className="main-layout">
        <Sidebar activeRoute="/hours" />
        <main className="main-content">
          <div className="page-header">
            <div className="page-header-left">
              <h1 className="page-title">Hour Logs</h1>
              <p className="page-subtitle">View your submitted hours</p>
            </div>
          </div>
          <div className="card">
            <div className="card-title">Your Hour Logs</div>
            <HourLogList />
          </div>
        </main>
      </div>
    </div>
  );
};
