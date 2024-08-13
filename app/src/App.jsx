import React, { useState } from 'react';
import MenuView from './pages/MenuView';
import TrendsView from './pages/TrendsView';
import LiveView from './pages/LiveView';
import CreditsView from './pages/CreditsView';
import SettingsView from './pages/SettingsView';
import './App.css';

const App = () => {
  const [currentPage, setCurrentPage] = useState('menu'); // 'menu' is the default page

  return (
    <div className="app-container">
      <nav>
        <button
          className={`nav-button ${currentPage === 'menu' ? 'active' : ''}`}
          onClick={() => setCurrentPage('menu')}
        >
          menu
        </button>
        <button
          className={`nav-button ${currentPage === 'trends' ? 'active' : ''}`}
          onClick={() => setCurrentPage('trends')}
        >
          trends
        </button>
        <button
          className={`nav-button ${currentPage === 'live' ? 'active' : ''}`}
          onClick={() => setCurrentPage('live')}
        >
          live
        </button>
        <button
          className={`nav-button ${currentPage === 'credits' ? 'active' : ''}`}
          onClick={() => setCurrentPage('credits')}
        >
          credits
        </button>
        <button
          className={`nav-button ${currentPage === 'settings' ? 'active' : ''}`}
          onClick={() => setCurrentPage('settings')}
        >
          settings
        </button>
      </nav>
      <main>
        {currentPage === 'menu' && <MenuView />}
        {currentPage === 'trends' && <TrendsView />}
        {currentPage === 'live' && <LiveView />}
        {currentPage === 'credits' && <CreditsView />}
        {currentPage === 'settings' && <SettingsView />}
      </main>
    </div>
  );
}

export default App;

