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
  const filteredlogs = logs.filter(picture => selectedBins.includes(picture.bin_id));

  return (
    <div style={styles.container}>
      <div>
        <h3>pictures</h3>
        <button 
          style={styles.toggleButton} 
          onClick={() => setShowFiltered(!showFiltered)}
        >
          Toggle {showFiltered ? 'Filtered' : 'Raw'} logs
        </button>
        <div>
          {selectedBins.length === 0 ? (
            <p>Select bins to display logs</p>
          ) : showFiltered ? (
            filteredlogs.map((picture, index) => (
              picture.filtered_picture ? (
                <div key={index} style={styles.pictureContainer}>
                  <p style={styles.timestamp}>{new Date(picture.timestamp).toLocaleString()}</p>
                  <img 
                    src={picture.filtered_picture} 
                    alt={`Filtered Picture ${index + 1}`} 
                    style={styles.image}
                  />
                </div>
              ) : null
            ))
          ) : (
            filteredlogs.map((picture, index) => (
              picture.raw_picture ? (
                <div key={index} style={styles.pictureContainer}>
                  <p style={styles.timestamp}>{new Date(picture.timestamp).toLocaleString()}</p>
                  <img 
                    src={picture.raw_picture} 
                    alt={`Raw Picture ${index + 1}`} 
                    style={styles.image}
                  />
                </div>
              ) : null
            ))
          )}
        </div>
      </div>
      <div>
        <h3>Options:</h3>
        <div>
          <h4>Bins</h4>
          {bins.map(bin => (
            <button
              key={bin.id}
              style={{
                backgroundColor: selectedBins.includes(bin.id) ? stringToColor(bin.name) : '#CCCCCC',
                color: getSpanColor(selectedBins.includes(bin.id) ? stringToColor(bin.name) : '#CCCCCC'),
                margin: '5px',
                padding: '10px',
                border: 'none',
                cursor: 'pointer',
                borderRadius: '12px',
              }}
              onClick={() => handleBinClick(bin.id)}
            >
              {bin.name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px',
  },
  toggleButton: {
    margin: '10px',
    padding: '10px',
    border: 'none',
    cursor: 'pointer',
    borderRadius: '12px',
    backgroundColor: '#CCCCCC',
  },
  pictureContainer: {
    margin: '10px',
    textAlign: 'center',
  },
  timestamp: {
    marginBottom: '5px',
    fontSize: '14px',
    color: '#555555',
  },
  image: {
    maxWidth: '100%',
    maxHeight: '400px',
    borderRadius: '8px',
  },
};

