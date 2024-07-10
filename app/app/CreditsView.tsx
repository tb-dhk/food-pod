import React from 'react';
import { View, TouchableOpacity, StyleSheet } from 'react-native';
import Text from '../components/Text.tsx'

export default function CreditsView({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>credits:</Text>
      <Text style={styles.text}>
        made by:{"\n"}
        - wang xinjie{"\n"}
        - johann young{"\n"}
        - keegan cheng{"\n"}
        - joshua soh{"\n"}
        - chen yixu{"\n\n"}
        special thanks to:{"\n"}
        - sembcorp industries{"\n"}
        - mr tiong heng liong{"\n"}
        - mr firdaus hamzah
      </Text>
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
  title: {
    fontSize: 25,
    marginBottom: 20,
  },
  text: {
    fontSize: 20,
    textAlign: 'center',
  },
});
