import React from 'react';
import { AuthProvider } from './context/AuthContext';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <div className="app">
        <h1>I-LEAD AMS</h1>
        <p>Frontend is being integrated with the production API...</p>
        <p>
          Check the console for logs. The API client is configured and ready for use.
        </p>
        <div className="info-box">
          <h2>Development Status</h2>
          <ul>
            <li>✅ API client configured with Axios</li>
            <li>✅ Auth context and hooks set up</li>
            <li>✅ All service modules created</li>
            <li>⏳ Components being migrated from legacy HTML</li>
            <li>⏳ React Router integration</li>
            <li>⏳ State management with Context</li>
          </ul>
        </div>
      </div>
    </AuthProvider>
  );
}

export default App;
