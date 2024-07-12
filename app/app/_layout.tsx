import React from 'react';
import { Stack } from "expo-router";
import { View, Image, StyleSheet } from "react-native";
import logo from "../assets/images/logo_horizontal_light.png"; // Ensure this is correct

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen 
        name="index" 
        options={{
          headerStyle: {
            backgroundColor: "#ffffff", 
          },
          headerTitle: () => {
            console.log('Rendering headerTitle'); // Debugging log
            return <View style={styles.container}><Image source={logo} style={styles.image} /></View>;
          },
          headerTitleAlign: 'center', // Center align the title if needed
        }}
      />
    </Stack>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center'
  },
  image: {
      flex: 1,
      width: 200,
      height: 50,
      resizeMode: 'contain'
  }
});
