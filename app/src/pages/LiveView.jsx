import React, { useState, useEffect } from 'react';
import fetchFromAzure from '../fetch.jsx';
import SHA256 from 'crypto-js/sha256';
import chroma from 'chroma-js'; // Import chroma-js for color manipulation

// Utility function to determine text color based on background color
const getSpanColor = (hexCode) => {
  const r = parseInt(hexCode.substr(1, 2), 16);
  const g = parseInt(hexCode.substr(3, 2), 16);
  const b = parseInt(hexCode.substr(5, 2), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 125 ? 'black' : 'white';
};

// Utility function to convert string to color using SHA256 hash and saturate
const stringToColor = (str) => {
  const hash = SHA256(str).toString();
  const color = `#${hash.substring(0, 6)}`;
  return chroma(color).saturate(1.5).darken(1.5).hex(); // Saturate and darken the color
};

export default function LiveView() {
  const [selectedBins, setSelectedBins] = useState([]);
  const [bins, setBins] = useState([]);
  const [logs, setLogs] = useState([]);
  const [showFiltered, setShowFiltered] = useState(true);

  // Function to handle bin item clicks
  const handleBinClick = (binId) => {
    if (selectedBins.includes(binId)) {
      setSelectedBins(selectedBins.filter(item => item !== binId));
    } else {
      setSelectedBins([...selectedBins, binId]);
    }
  };

  // Function to load data from Azure SQL
  const loadData = async () => {
    try {
      const binsData = await fetchFromAzure('bins');
      setBins(binsData);
      
      const logsData = await fetchFromAzure('logs');
      setLogs(logsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // Effect to fetch initial data
  useEffect(() => {
    loadData();
  }, []);

  // Filter logs based on selected bins
  const filteredLogs = logs.filter(log => selectedBins.includes(log.bin_id));

  return (
    <div className="container">
      <div className="two-column-layout">
        <div className="option-buttons">
          <h3>Bins</h3>
          {bins.map(bin => (
            <button
              key={bin.id}
              className="option-button"
              style={{
                backgroundColor: selectedBins.includes(bin.id) ? stringToColor(bin.name) : '#CCCCCC',
                color: getSpanColor(selectedBins.includes(bin.id) ? stringToColor(bin.name) : '#CCCCCC'),
              }}
              onClick={() => handleBinClick(bin.id)}
            >
              {bin.name}
            </button>
          ))}
        </div>
        <div className="content">
          <h3>Pictures</h3>
          <button 
            className="toggle-button" 
            onClick={() => setShowFiltered(!showFiltered)}
          >
            toggle {showFiltered ? 'filtered' : 'raw'} logs
          </button>
          <div class={`logs-container ${selectedBins.length ? "grid" : ""}`}>
            {selectedBins.length === 0 ? (
              <p>Select bins to display logs.</p>
            ) : showFiltered ? (
              filteredLogs.map((log, index) => (
                log.filtered_picture ? (
                  <div key={index} className="picture-container">
                    <p className="timestamp">{new Date(log.timestamp).toLocaleString()}</p>
                    <img 
                      src={log.filtered_picture} 
                      alt={`Filtered Picture ${index + 1}`}
                    />
                  </div>
                ) : null
              ))
            ) : (
              filteredLogs.map((log, index) => (
                log.raw_picture ? (
                  <div key={index} className="picture-container">
                    <p className="timestamp">{new Date(log.timestamp).toLocaleString()}</p>
                    <img 
                      src={log.raw_picture} 
                      alt={`Raw Picture ${index + 1}`} 
                    />
                  </div>
                ) : null
              ))
            )}
          </div>    
        </div>
      </div>
    </div>
  );
}

