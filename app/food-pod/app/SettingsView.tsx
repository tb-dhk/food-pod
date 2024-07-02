import React from 'react';
import { View, TouchableOpacity, StyleSheet } from 'react-native';
import Text from '../components/Text'

export default function SettingsView({ navigation }) {
  return (
    <View style={styles.container}>
      <Text>Settings</Text>
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
});
