import React, { useState, useEffect } from 'react';
import { View, TouchableOpacity, ScrollView, StyleSheet, Dimensions } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { SHA256 } from 'crypto-js';
import Text from '../components/Text';
import db from './knexConfig';

const fetchBinsData = async () => {
  try {
    const binsData = await db.select('*').from('Bins');
    return binsData;
  } catch (error) {
    console.error('Error fetching bins data:', error);
    throw error;
  }
};

const fetchFoodData = async (startDate, endDate, bins) => {
  try {
    const foodData = await db('Food')
      .select('*')
      .whereBetween('Date', [startDate, endDate])
      .whereIn('BinId', bins);
    
    return foodData;
  } catch (error) {
    console.error('Error fetching food data:', error);
    throw error;
  }
};

export default function TrendsView({ navigation }) {
  const [selectedFoods, setSelectedFoods] = useState([]);
  const [blendedColor, setBlendedColor] = useState('#CCCCCC');
  const [foodData, setFoodData] = useState([]);
  const [bins, setBins] = useState([]);

  const handleFoodClick = (food) => {
    if (selectedFoods.includes(food)) {
      setSelectedFoods(selectedFoods.filter(item => item !== food));
    } else {
      setSelectedFoods([...selectedFoods, food]);
    }
  };

  useEffect(() => {
    const fetchInitialData = () => {
      fetchFoodData(startDate, endDate, selectedBins);
      fetchBinsData().then(data => setBins(data));
    };
    fetchInitialData();
  }, []);

  useEffect(() => {
    const colors = selectedFoods.map(food => "#" + SHA256(food).toString().substring(0, 6));
    setBlendedColor(colors.length > 0 ? blendColors(colors) : '#CCCCCC');
  }, [selectedFoods]);

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

  const rgbToHex = (rgb) => {
    const r = Math.round(rgb[0]);
    const g = Math.round(rgb[1]);
    const b = Math.round(rgb[2]);
    return `#${(r << 16 | g << 8 | b).toString(16).padStart(6, '0')}`;
  };

  const hexToRgb = (hex) => {
    const r = parseInt(hex.substr(1, 2), 16);
    const g = parseInt(hex.substr(3, 2), 16);
    const b = parseInt(hex.substr(5, 2), 16);
    return [r, g, b];
  };

  const renderLineChart = () => {
    if (selectedFoods.length > 0) {
      return (
        <LineChart
          data={{
            labels: foodData[selectedFoods[0]].map(d => new Date(d.time).toLocaleDateString()),
            datasets: selectedFoods.map(food => ({
              data: foodData[food].map(d => d.weight),
              color: () => `rgba(${hexToRgb("#" + SHA256(food).toString().substring(0, 6)).join(',')}, 1)`
            }))
          }}
          width={Dimensions.get('window').width - 30}
          height={250}
          chartConfig={{
            backgroundColor: blendedColor,
            backgroundGradientFrom: blendedColor,
            backgroundGradientTo: blendedColor,
            decimalPlaces: 2,
            color: () => getTextColor(blendedColor),
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
          data={{
            labels: [],
            datasets: [{ data: [] }]
          }}
          fromZero
          width={Dimensions.get('window').width - 30}
          height={250}
          chartConfig={{
            backgroundColor: '#CCCCCC',
            backgroundGradientFrom: '#CCCCCC',
            backgroundGradientTo: '#CCCCCC',
            decimalPlaces: 2,
            color: () => getTextColor('#CCCCCC'),
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
    <View style={styles.container}>
      {renderLineChart()}
      <ScrollView horizontal style={styles.buttonContainer}>
        {Object.keys(foodData).map((item, index) => (
          <TouchableOpacity
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
            <Text style={{ color: getTextColor(selectedFoods.includes(item) ? "#" + SHA256(item).toString().substring(0, 6) : '#CCCCCC') }}>{item}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
      <ScrollView horizontal style={styles.buttonContainer}>
        {bins.map((bin, index) => (
          <TouchableOpacity
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
            <Text style={{ color: getTextColor(selectedFoods.includes(bin.name) ? "#" + SHA256(bin.name).toString().substring(0, 6) : '#CCCCCC') }}>{bin.name}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
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

const getTextColor = (hexCode) => {
  const r = parseInt(hexCode.substr(1, 2), 16);
  const g = parseInt(hexCode.substr(3, 2), 16);
  const b = parseInt(hexCode.substr(5, 2), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 125 ? 'black' : 'white';
};

