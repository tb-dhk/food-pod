import { Link, Stack } from 'expo-router';
import { StyleSheet } from 'react-native';

import { Themedspan } from '@/components/Themedspan';
import { Themeddiv } from '@/components/Themeddiv';

export default function NotFoundScreen() {
  return (
    <>
      <Stack.Screen options={{ title: 'Oops!' }} />
      <Themeddiv style={styles.container}>
        <Themedspan type="title">This screen doesn't exist.</Themedspan>
        <Link href="/" style={styles.link}>
          <Themedspan type="link">Go to home screen!</Themedspan>
        </Link>
      </Themeddiv>
    </>
  );
}

const styles =({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  link: {
    marginTop: 15,
    paddingVertical: 15,
  },
});
