import React, { useState } from 'react';
import MenuView from './pages/MenuView';
import TrendsView from './pages/TrendsView';
import LiveView from './pages/LiveView';
import CreditsView from './pages/CreditsView';
import SettingsView from './pages/SettingsView';

const App = () => {
  const [currentPage, setCurrentPage] = useState('menu'); // 'menu' is the default page

  return (
    <div>
      <nav>
        <button onClick={() => setCurrentPage('menu')}>Menu</button>
        <button onClick={() => setCurrentPage('trends')}>Trends</button>
        <button onClick={() => setCurrentPage('live')}>Live</button>
        <button onClick={() => setCurrentPage('credits')}>Credits</button>
        <button onClick={() => setCurrentPage('settings')}>Settings</button>
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

