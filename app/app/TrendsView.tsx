import React, { useState, useEffect } from 'react';
import { View, TouchableOpacity, ScrollView, StyleSheet } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';
import { SHA256 } from 'crypto-js';
import Text from '../components/Text'

const data = {
  "apples": [
    { "time": "6/1/2021", "weight": 5 },
    { "time": "6/5/2021", "weight": 7 },
    { "time": "6/10/2021", "weight": 6 },
    { "time": "6/15/2021", "weight": 4 }
  ],
  "bananas": [
    { "time": "6/2/2021", "weight": 2 },
    { "time": "6/6/2021", "weight": 3 },
    { "time": "6/11/2021", "weight": 1 },
    { "time": "6/16/2021", "weight": 4 }
  ],
  "carrots": [
    { "time": "6/3/2021", "weight": 8 },
    { "time": "6/7/2021", "weight": 5 },
    { "time": "6/12/2021", "weight": 7 },
    { "time": "6/17/2021", "weight": 6 }
  ]
}

function getTextColor(hexCode) {
  // Convert hex to RGB
  const r = parseInt(hexCode.substr(1, 2), 16);
  const g = parseInt(hexCode.substr(3, 2), 16);
  const b = parseInt(hexCode.substr(5, 2), 16);

  // Calculate relative luminance (perceptual brightness)
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;

  // Decide text color based on luminance
  return luminance > 0.5 ? '#000000' : '#FFFFFF'; // Black for light backgrounds, white for dark backgrounds
}

export default function TrendsView({ navigation }) {
  const [selectedFoods, setSelectedFoods] = useState([]);
  const [blendedColor, setBlendedColor] = useState('#CCCCCC'); // Initial blended color is grey

  const handleFoodClick = (food) => {
    // Toggle food selection
    if (selectedFoods.includes(food)) {
      setSelectedFoods(selectedFoods.filter(item => item !== food));
    } else {
      setSelectedFoods([...selectedFoods, food]);
    }
  };

  // Update selected colors and blended color whenever selectedFoods changes
  useEffect(() => {
    const colors = selectedFoods.map(food => "#" + SHA256(food).toString().substring(0, 6));
    setBlendedColor(colors.length > 0 ? blendColors(colors) : '#CCCCCC');
  }, [selectedFoods]);

  const blendColors = (colors) => {
    const rgbaColors = [...colors.map(hexToRgb), [255, 255, 255]]; // Add [255, 255, 255] for white
    const avgColor = rgbaColors.reduce((acc, color) => {
      return [
        acc[0] + color[0] / rgbaColors.length,
        acc[1] + color[1] / rgbaColors.length,
        acc[2] + color[2] / rgbaColors.length
      ];
    }, [0, 0, 0]);

    // Convert average RGB to hex
    const hexColor = rgbToHex(avgColor);
    return hexColor;
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
            labels: data[selectedFoods[0]].map(d => new Date(d.time).toLocaleDateString()),
            datasets: selectedFoods.map(food => ({
              data: data[food].map(d => d.weight),
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
            backgroundColor: '#CCCCCC', // Grey background when no food items selected
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
        {Object.keys(data).map((item, index) => (
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

