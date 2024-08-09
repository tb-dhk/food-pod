import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';  // Import your CSS file
import App from './App'; // Import the main App component

// Create the root element for rendering
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component inside the root element
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

