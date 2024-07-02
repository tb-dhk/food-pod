import React from 'react';
import { View, TouchableOpacity, Image, StyleSheet } from 'react-native';
import Text from '../components/Text'

export default function MenuView({  }) {
  return (
    <View style={styles.container}>
      <Text>welcome to the food:pod app!</Text>

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
  logo: {
    height: "40%",
    width: 200,
    marginBottom: 20,
  },
});

