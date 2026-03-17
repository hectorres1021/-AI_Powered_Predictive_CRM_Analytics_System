import React from 'react';
import { Navbar } from '../components/Layout/Navbar';
import { Sidebar } from '../components/Layout/Sidebar';

export const UsersPage = () => {
  return (
    <div className="app-main">
      <Navbar />
      <div className="main-layout">
        <Sidebar activeRoute="/users" />
        <main className="main-content">
          <div className="page-header">
            <h1 className="page-title">Users</h1>
            <p className="page-subtitle">Manage system users and roles</p>
          </div>
          <div className="card">
            <p>Users component coming soon...</p>
          </div>
        </main>
      </div>
    </div>
  );
};
