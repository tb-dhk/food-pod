import React, { useState, useEffect } from 'react';
import { SHA256 } from 'crypto-js'; // Import crypto-js for hashing if needed
import { LineChart } from '@mui/x-charts';
import fetchFromAzure from '../fetch.jsx'
import chroma from 'chroma-js'; // Import chroma-js for color manipulation

// Utility function to determine text color based on background color
const getSpanColor = (hexCode) => {
  const r = parseInt(hexCode.substr(1, 2), 16);
  const g = parseInt(hexCode.substr(3, 2), 16);
  const b = parseInt(hexCode.substr(5, 2), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 125 ? 'black' : 'white';
};

// Utility function to blend colors, including black and white
const blendColors = (colors, layer = 0) => {
  if (!colors.length) {
    return "#cccccc";
  }

  let r = 0, g = 0, b = 0;

  colors.forEach(color => {
    const hex = color.replace('#', '');
    r += parseInt(hex.substr(0, 2), 16);
    g += parseInt(hex.substr(2, 2), 16);
    b += parseInt(hex.substr(4, 2), 16);
  });

  r = Math.round(r / colors.length);
  g = Math.round(g / colors.length);
  b = Math.round(b / colors.length);

  if (layer === 0) {
    return blendColors([`#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`, "#ffffff", "#ffffff", "#ffffff"], layer = 1);
  } else {
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
  }
};

// Utility function to convert string to color using SHA256 hash and saturate
const stringToColor = (str) => {
  const hash = SHA256(str).toString();
  const color = `#${hash.substring(0, 6)}`;
  return chroma(color).saturate(1.5).darken(1.5).hex(); // Saturate and darken the color
};

export default function Trendsdiv({ navigation }) {
  const [selectedFoods, setSelectedFoods] = useState([]);
  const [selectedBins, setSelectedBins] = useState([]); // Added state for selected bins
  const [bins, setBins] = useState([]);
  const [logs, setLogs] = useState([]);
  const [food, setFood] = useState([]);
  const [blendedColor, setBlendedColor] = useState('#CCCCCC');

  // Function to handle food item clicks
  const handleFoodClick = (foodId) => {
    if (selectedFoods.includes(foodId)) {
      setSelectedFoods(selectedFoods.filter(item => item !== foodId));
    } else {
      setSelectedFoods([...selectedFoods, foodId]);
    }
  };

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
      const logsData = await fetchFromAzure('logs');
      setLogs(logsData);
      console.log("logs:", logsData);

      const foodData = await fetchFromAzure('food');
      setFood(foodData);
      console.log("food:", foodData);

      const binData = await fetchFromAzure('bins');
      setBins(binData);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // Effect to fetch initial data
  useEffect(() => {
    loadData();
  }, []);

  // Effect to process data and update blendedColor
  useEffect(() => {
    setBlendedColor(blendColors(selectedFoods.map(foodId => stringToColor(food[foodId - 1].name))));
  }, [logs, food, selectedFoods]);

  // Render the LineChart
  const processAndPrepareChartData = (logs, selectedFoods, selectedBins) => {
    const foodDataMap = {};
    
    // Find the earliest date
    const earliestDate = new Date(Math.min(...logs.map(log => new Date(log.timestamp))));
    console.log("Earliest Date:", earliestDate.toLocaleDateString());

    logs.forEach(log => {
      if (selectedBins.length && !selectedBins.includes(log.bin_id)) {
        return;
      }

      console.log("Processing log:", log.timestamp, log.estimated_amts_of_food);

      const foodEstimates = JSON.parse(log.estimated_amts_of_food);
      const logDate = new Date(log.timestamp);
      const daysSinceEarliest = Math.floor((logDate - earliestDate) / (1000 * 60 * 60 * 24));
      console.log("Days since earliest:", daysSinceEarliest);

      Object.keys(foodEstimates).forEach(foodId => {
        const parsedFoodId = parseInt(foodId);
        if (selectedFoods.includes(parsedFoodId) && selectedBins.includes(parseInt(log.bin_id))) {
          if (!foodDataMap[parsedFoodId]) {
            foodDataMap[parsedFoodId] = {};
          }

          const amount = foodEstimates[parsedFoodId];
          if (foodDataMap[parsedFoodId][daysSinceEarliest]) {
            foodDataMap[parsedFoodId][daysSinceEarliest] += amount;
          } else {
            foodDataMap[parsedFoodId][daysSinceEarliest] = amount;
          }
          console.log(`Updated foodDataMap[${parsedFoodId}]`, foodDataMap[parsedFoodId]);
        }
      });
    });

    console.log("Food Data Map:", foodDataMap);

    // Prepare chart data
    const xAxis = [{ data: [] }];
    const series = [];

    // Find the start and end days based on all food data
    const allDays = [];
    Object.values(foodDataMap).forEach(data => {
      allDays.push(...Object.keys(data).map(day => parseInt(day)));
    });
    const minDay = Math.min(...allDays);
    const maxDay = Math.max(...allDays);

    // Ensure xAxis includes all days from minDay to maxDay
    for (let i = minDay; i <= maxDay; i++) {
      if (!xAxis[0].data.includes(i)) {
        xAxis[0].data.push(i);
        console.log(`Added ${i} to xAxis`);
      }
    }

    // Iterate over each foodId in the foodDataMap
    Object.entries(foodDataMap).forEach(([foodId, data]) => {
      const foodSeries = [];
      
      console.log(`Processing data for foodId ${foodId}`);
      console.log(`Days:`, xAxis[0].data);

      // Initialize foodSeries with zeros for each day from minDay to maxDay
      xAxis[0].data.forEach(day => {
        foodSeries.push(data[day] !== undefined ? data[day] : 0);
        console.log(`Day ${day}: Added ${data[day] !== undefined ? data[day] : 0} to foodSeries`);
      });

      console.log(`Series for foodId ${foodId}:`, foodSeries);

      series.push({
        data: foodSeries,
        name: food[parseInt(foodId) - 1].name,
        type: 'line',
        smooth: true,
        color: stringToColor(food[parseInt(foodId) - 1].name),
      });
    });

    return { series, xAxis, foodDataMap, earliestDate };
  };

  const { series, xAxis, foodDataMap, earliestDate } = processAndPrepareChartData(logs, selectedFoods, selectedBins);

  // Create the table data from the foodDataMap
  const tableData = Object.entries(foodDataMap).map(([foodId, data]) => {
    return {
      foodName: food[parseInt(foodId) - 1].name,
      ...xAxis[0].data.reduce((acc, day) => {
        acc[`Day ${day}`] = data[day] !== undefined ? data[day] : 0;
        return acc;
      }, {})
    };
  });

  return (
    <div style={{...styles.container, backgroundColor: blendedColor}}>
      <div>
        <h3>graph</h3>
        <LineChart
          series={series}
          xAxis={xAxis}
          height={400}
          width={600}
          title="food waste over time"
          noDataOverlay="no data to display"
        />
      </div>
      <div>
        <h3>data table</h3>
        {tableData.length > 0 ? (
          <table border="1" style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>Food Name</th>
                {xAxis[0].data.map(day => (
                  <th key={day}>Day {day}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData.map((row, index) => (
                <tr key={index}>
                  <td>{row.foodName}</td>
                  {xAxis[0].data.map(day => (
                    <td key={day}>{row[`Day ${day}`]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>no data to display</p>
        )}
      </div>
      <div>
        <h3>options:</h3>
        <div>
          <h4>foods</h4>
          {food.map(item => (
            <button
              key={item.id}
              style={{
                backgroundColor: selectedFoods.includes(item.id) ? stringToColor(item.name) : '#CCCCCC',
                color: getSpanColor(selectedFoods.includes(item.id) ? stringToColor(item.name) : '#CCCCCC'),
                margin: '5px',
                padding: '10px',
                border: 'none',
                cursor: 'pointer',
                borderRadius: '12px',
              }}
              onClick={() => handleFoodClick(item.id)}
            >
              {item.name}
            </button>
          ))}
        </div>
        <div>
          <h4>bins</h4>
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
};

