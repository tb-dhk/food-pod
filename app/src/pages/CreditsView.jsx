import React from 'react'

export default function Creditsdiv({ navigation }) {
  return (
    <div style={styles.container}>
      <span style={styles.title}>credits:</span>
      <span style={styles.text}>
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
      </span>
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
  title: {
    fontSize: 25,
    marginBottom: 20,
  },
  text: {
    fontSize: 20,
    textAlign: 'center',
  },
});
