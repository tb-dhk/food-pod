import React, { useState, useEffect } from 'react';
import { SHA256 } from 'crypto-js'; // Import crypto-js for hashing if needed
import { LineChart } from '@mui/x-charts';
import axios from 'axios'; // Import axios for making HTTP requests
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
const blendColors = (colors, layer=0) => {
  if (!colors.length) {
    return "#800000"
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

  if (layer == 0) {
    return blendColors([`#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`, "#ffffff", "#ffffff"], layer=1);
  } else {
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`
  }
};

// Utility function to convert string to color using SHA256 hash and saturate
const stringToColor = (str) => {
  const hash = SHA256(str).toString();
  const color = `#${hash.substring(0, 6)}`;
  return chroma(color).saturate(1.5).darken(1.5).hex(); // Saturate the color
};

// Function to fetch data from an Azure SQL database
async function fetchFromAzure(endpoint) {
  try {
    const response = await axios.get(`https://localhost:5000/api/${endpoint}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching data from Azure:', error);
    return [];
  }
}

export default function Trendsdiv({ navigation }) {
  const [selectedFoods, setSelectedFoods] = useState([]);
  const [bins, setBins] = useState([]);
  const [logs, setLogs] = useState([]);
  const [food, setFood] = useState([]);
  const [blendedColor, setBlendedColor] = useState('#CCCCCC');

  // Function to handle food item clicks
  const handleFoodClick = (food) => {
    if (selectedFoods.includes(food)) {
      setSelectedFoods(selectedFoods.filter(item => item !== food));
    } else {
      setSelectedFoods([...selectedFoods, food]);
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
    if (logs.length === 0 || food.length === 0 || selectedFoods.length === 0) {
      return;
    }

    setBlendedColor(blendColors(selectedFoods.map(foodId => stringToColor(food[foodId - 1].name))));
  }, [logs, food, selectedFoods]);

  // Render the LineChart
  const processAndPrepareChartData = (logs, selectedFoods) => {
    const foodDataMap = {};
    
    // Find the earliest date
    const earliestDate = new Date(Math.min(...logs.map(log => new Date(log.timestamp))));
    console.log("Earliest Date:", earliestDate.toLocaleDateString());

    logs.forEach(log => {
      console.log("Processing log:", log.timestamp, log.estimated_amts_of_food);

      const foodEstimates = JSON.parse(log.estimated_amts_of_food);
      const logDate = new Date(log.timestamp);
      const daysSinceEarliest = Math.floor((logDate - earliestDate) / (1000 * 60 * 60 * 24));
      console.log("Days since earliest:", daysSinceEarliest);

      Object.keys(foodEstimates).forEach(foodId => {
        const parsedFoodId = parseInt(foodId);
        if (selectedFoods.includes(parsedFoodId)) {
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
      })
    });

    return { series, xAxis };
  };

  const { series, xAxis } = processAndPrepareChartData(logs, selectedFoods);

  return (
    <div style={{ ...styles.container, backgroundColor: blendedColor }}>
      <LineChart
        width={window.innerWidth - 30}
        height={250}
        series={series}
        xAxis={xAxis}
        dataset={[{}]}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      />
      <div style={styles.buttonContainer}>
        {Object.keys(food).map((item, index) => (
          <button
            key={index}
            onClick={() => handleFoodClick(parseInt(item) + 1)}
            style={{
              backgroundColor: selectedFoods.includes(parseInt(item) + 1) ? stringToColor(food[item].name) : '#ccc',
              color: getSpanColor(selectedFoods.includes(parseInt(item) + 1) ? stringToColor(food[item].name) : '#ccc')
            }}
          >
            {food[item]?.name || `Food ${item}`}
          </button>
        ))}
      </div>
    </div>
  );
}

// Styles for the container
const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
    padding: '20px',
  },
  buttonContainer: {
    flexDirection: 'row',
    marginTop: 20,
  }
};

