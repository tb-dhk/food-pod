import React, { useState, useEffect, useRef } from 'react';
import { SHA256 } from 'crypto-js'; // Import crypto-js for hashing if needed
import { LineChart } from '@mui/x-charts';
import fetchFromAzure from '../fetch.jsx';
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
  if (colors.length === 0) {
    return "#ffffff";
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
    return blendColors([`#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`, "#ffffff", "#ffffff", "#ffffff", "#ffffff"], layer = 1);
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

export default function Trendsdiv({ props }) {
  const [selectedFoods, setSelectedFoods] = useState([]);
  const [selectedBins, setSelectedBins] = useState([]);
  const [bins, setBins] = useState([]);
  const [logs, setLogs] = useState([]);
  const [food, setFood] = useState([]);
  const [blendedColor, setBlendedColor] = useState('#CCCCCC');
  const chartContainerRef = useRef(null);
  const [chartWidth, setChartWidth] = useState(600);

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

      const foodData = await fetchFromAzure('food');
      setFood(foodData);

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
    setBlendedColor(blendColors(selectedFoods.map(foodId => stringToColor(food[foodId - 1].name)).concat(selectedBins.map(binId => stringToColor(bins[binId - 1].name)))));
  }, [logs, food, selectedFoods]);

  // Effect to update chart width based on parent container size
  useEffect(() => {
    const updateChartWidth = () => {
      if (chartContainerRef.current) {
        setChartWidth(chartContainerRef.current.offsetWidth * 0.8);
      }
    };

    updateChartWidth();
    window.addEventListener('resize', updateChartWidth);

    return () => window.removeEventListener('resize', updateChartWidth);
  }, []);

  // Render the LineChart
  const processAndPrepareChartData = (logs, selectedFoods, selectedBins) => {
    const foodDataMap = {};
    
    // Find the earliest date
    const earliestDate = new Date(Math.min(...logs.map(log => new Date(log.timestamp))));

    logs.forEach(log => {
      if (selectedBins.length && !selectedBins.includes(log.bin_id)) {
        return;
      }

      const foodEstimates = JSON.parse(log.estimated_amts_of_food);
      const logDate = new Date(log.timestamp);
      const daysSinceEarliest = Math.floor((logDate - earliestDate) / (1000 * 60 * 60 * 24));

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
        }
      });
    });

    // Prepare chart data
    const xAxis = [{ data: [], label: "time (days)" }];
    let series = [];

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
      }
    }

    // Iterate over each foodId in the foodDataMap
    Object.entries(foodDataMap).forEach(([foodId, data]) => {
      const foodSeries = [];

      // Initialize foodSeries with zeros for each day from minDay to maxDay
      xAxis[0].data.forEach(day => {
        foodSeries.push(data[day] !== undefined ? data[day] : 0);
      });

      series.push({
        curve: "catmullRom",
        data: foodSeries,
        name: food[parseInt(foodId) - 1].name,
        smooth: true,
        color: stringToColor(food[parseInt(foodId) - 1].name),
        id: foodId
      });

      series = series.sort((a, b) => a.id - b.id)
    });

    return { series, xAxis, foodDataMap, earliestDate };
  };

  const { series, xAxis, foodDataMap, earliestDate } = processAndPrepareChartData(logs, selectedFoods, selectedBins);

  // Create the table data from the foodDataMap
  const tableData = Object.entries(foodDataMap).map(([foodId, data]) => {
    return {
      foodName: food[parseInt(foodId) - 1].name,
      ...xAxis[0].data.reduce((acc, day) => {
        acc[`day ${day}`] = data[day] !== undefined ? data[day] : 0;
        return acc;
      }, {})
    };
  });

  return (
    <div className="container">
      <div className="two-column-layout">
        <div className="option-buttons">
          <h3>food</h3>
          <div>
            {food.map((foodItem) => {
              const color = stringToColor(foodItem.name);
              return (
                <button
                  key={foodItem.id}
                  className={`option-button ${selectedFoods.includes(foodItem.id) ? 'selected' : ''}`}
                  onClick={() => handleFoodClick(foodItem.id)}
                  style={{
                    backgroundColor: selectedFoods.includes(foodItem.id) ? color : 'inherit',
                    color: selectedFoods.includes(foodItem.id) ? getSpanColor(color) : 'inherit',
                    borderColor: color
                  }}
                >
                  {foodItem.name}
                </button>
              );
            })}
          </div>
          <h3>bins</h3>
          <div>
            {bins.map((binItem) => {
              const color = stringToColor(binItem.name);
              return (
                <button
                  key={binItem.id}
                  className={`option-button ${selectedBins.includes(binItem.id) ? 'selected' : ''}`}
                  onClick={() => handleBinClick(binItem.id)}
                  style={{
                    backgroundColor: selectedBins.includes(binItem.id) ? color : 'inherit',
                    color: selectedBins.includes(binItem.id) ? getSpanColor(color) : 'inherit',
                    borderColor: color
                  }}
                >
                  {binItem.name}
                </button>
              );
            })}
          </div>
        </div>
        <div className="content" style={{backgroundColor: blendedColor, display: "flex", justifyContent: "center", flexDirection: "column"}} ref={chartContainerRef}>
          <LineChart
            title="Food Wastage Over Time"
            width={chartWidth}
            height={400}
            series={series}
            xAxis={xAxis}
            yAxis={[{ label: "amount (g)" }]}
            sx={{
              "& .css-1f57y8b": {
                fontFamily: "Comfortaa"
              }
            }}
            noDataOverlay="no data to display"
          />
          {tableData.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>food name</th>
                  {xAxis[0].data.map((day, index) => (
                    <th key={index}>{`day ${day}`}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tableData.map((row, index) => (
                  <tr key={index}>
                    <td>{row.foodName}</td>
                    {xAxis[0].data.map((day, index) => (
                      <td key={index}>{row[`day ${day}`]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>no data to display</p>
          )}
        </div>
      </div>
    </div>
  );
}

