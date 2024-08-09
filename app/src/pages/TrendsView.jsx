import React, { useState, useEffect } from 'react';
import { SHA256 } from 'crypto-js'; // Import crypto-js for hashing if needed
import { LineChart } from "@mui/x-charts"
import axios from 'axios'; // Import axios for making HTTP requests

// Utility function to determine text color based on background color
const getSpanColor = (hexCode) => {
  const r = parseInt(hexCode.substr(1, 2), 16);
  const g = parseInt(hexCode.substr(3, 2), 16);
  const b = parseInt(hexCode.substr(5, 2), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 125 ? 'black' : 'white';
}

// Function to fetch data from an Azure SQL database
async function fetchFromAzure(endpoint) {
  try {
    const response = await axios.get(`https://food-pod.onrender.com/api/${endpoint}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching data from Azure:', error);
    return [];
  }
}

// Define your component
export default function Trendsdiv({ navigation }) {
  const [selectedFoods, setSelectedFoods] = useState([]);
  const [startDate, setStartDate] = useState(''); // Initialize as an empty string
  const [endDate, setEndDate] = useState('');     // Initialize as an empty string
  const [bins, setBins] = useState([]);
  const [logs, setLogs] = useState([]);
  const [food, setFood] = useState([]);
  const [blendedColor, setBlendedColor] = useState('#CCCCCC');
  const [foodData, setFoodData] = useState([]);

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

  const blendColors = (colors) => {
    const rgbaColors = [...colors.map(hexToRgb), [255, 255, 255]];
    const avgColor = rgbaColors.reduce((acc, color) => {
      return [
        acc[0] + color[0] / rgbaColors.length,
        acc[1] + color[1] / rgbaColors.length,
        acc[2] + color[2] / rgbaColors.length
      ];
    }, [0, 0, 0]);

    return rgbToHex(avgColor);
  };

  useEffect(() => {
    const colors = selectedFoods.map(food => "#" + SHA256(food).toString().substring(0, 6));
    setBlendedColor(colors.length > 0 ? blendColors(colors) : '#CCCCCC');
  }, [selectedFoods]);

  const rgbToHex = (rgb) => {
    const r = Math.round(rgb[0]);
    const g = Math.round(rgb[1]);
    const b = Math.round(rgb[2]);
    return `#${((r << 16) | (g << 8) | b).toString(16).padStart(6, '0')}`;
  };

  const hexToRgb = (hex) => {
    const r = parseInt(hex.substr(1, 2), 16);
    const g = parseInt(hex.substr(3, 2), 16);
    const b = parseInt(hex.substr(5, 2), 16);
    return [r, g, b];
  };

  const renderLineChart = () => {
    let dataset = {};

    if (selectedFoods.length > 0) {
      dataset = selectedFoods.map(food => ({
        data: foodData[food].map(d => ({ x: new Date(d.time).toLocaleDateString(), y: d.weight })),
      }));

      return (
        <LineChart
          xAxis={[{ dataKey: 'x' }]}
          series={[]}
          dataset={dataset.map((data, index) => ({
            dataKey: 'y',
            data: data.data,
            color: () => `rgba(${hexToRgb("#" + SHA256(selectedFoods[index]).toString().substring(0, 6)).join(',')}, 1)`
          }))}
          width={window.innerWidth - 30}
          height={250}
          chartConfig={{
            backgroundColor: blendedColor,
            backgroundGradientFrom: blendedColor,
            backgroundGradientTo: blendedColor,
            decimalPlaces: 2,
            color: () => getSpanColor(blendedColor),
            style: {
              borderRadius: 16
            },
            propsForLabels: {
              fontFamily: "Comfortaa"
            }
          }}
          style={{
            padding: 10,
            borderRadius: 16
          }}
        />
      );
    } else {
      return (
        <LineChart
          xAxis={[{ dataKey: 'x' }]}
          series={[]}
          dataset={[{
            dataKey: 'y',
            data: []
          }]}
          width={window.innerWidth - 30}
          height={250}
          chartConfig={{
            backgroundColor: '#CCCCCC',
            backgroundGradientFrom: '#CCCCCC',
            backgroundGradientTo: '#CCCCCC',
            decimalPlaces: 2,
            color: () => getSpanColor('#CCCCCC'),
            style: {
              borderRadius: 16
            },
            propsForLabels: {
              fontFamily: "Comfortaa"
            }
          }}
          style={{
            padding: 10,
            borderRadius: 16
          }}
        />
      );
    }
  };

  return (
    <div style={styles.container}>
      {renderLineChart()}
      <div horizontal style={styles.buttonContainer}>
        {Object.keys(foodData).map((item, index) => (
          <button
            key={index}
            onPress={() => handleFoodClick(item)}
            style={{
              backgroundColor: selectedFoods.includes(item) ? "#" + SHA256(item).toString().substring(0, 6) : '#CCCCCC',
              height: 50,
              margin: 10,
              padding: 10,
              justifyContent: "center",
              alignItems: "center",
              borderRadius: 8
            }}
          >
            <span style={{ color: getSpanColor(selectedFoods.includes(item) ? "#" + SHA256(item).toString().substring(0, 6) : '#CCCCCC') }}>{item}</span>
          </button>
        ))}
      </div>
      <div horizontal style={styles.buttonContainer}>
        {bins.map((bin, index) => (
          <button
            key={index}
            onPress={() => handleFoodClick(bin.name)}
            style={{
              backgroundColor: selectedFoods.includes(bin.name) ? "#" + SHA256(bin.name).toString().substring(0, 6) : '#CCCCCC',
              height: 50,
              margin: 10,
              padding: 10,
              justifyContent: "center",
              alignItems: "center",
              borderRadius: 8
            }}
          >
            <span style={{ color: getSpanColor(selectedFoods.includes(bin.name) ? "#" + SHA256(bin.name).toString().substring(0, 6) : '#CCCCCC') }}>{bin.name}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

const styles = ({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'antiquewhite',
  },
  buttonContainer: {
    flexDirection: 'row',
    marginVertical: 20,
  },
});

