import React from 'react'

export default function Settingsdiv({ navigation }) {
  return (
    <div style={styles.container}>
      <span>Settings</span>
    </div>
  );
}

const styles =({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'antiquewhite',
  },
});
