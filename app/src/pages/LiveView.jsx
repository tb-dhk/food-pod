import React from 'react'

export default function Livediv({ navigation }) {
  return (
    <div style={styles.container}>
      <span>live feed</span>
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
});
