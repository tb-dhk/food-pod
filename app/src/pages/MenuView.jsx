import React from 'react'

export default function Menudiv() {
  return (
    <div style={styles.container}>
      <span>welcome to the food:pod app!</span>
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
  logo: {
    height: "40%",
    width: 200,
    marginBottom: 20,
  },
});

