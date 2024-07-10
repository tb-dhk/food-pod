import React from 'react';
import { Text as RNText, StyleSheet } from 'react-native';

export default function Text(props) {
  return <RNText {...props} style={[styles.text, props.style]} />;
}

const styles = StyleSheet.create({
  text: {
    fontFamily: 'Comfortaa',
  },
});

