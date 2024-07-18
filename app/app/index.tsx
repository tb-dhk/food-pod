import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import MenuView from './MenuView';
import TrendsView from './TrendsView';
import SettingsView from './SettingsView';
import LiveView from './LiveView';
import CreditsView from './CreditsView';

const Tab = createBottomTabNavigator();
export default function App() {
  return (
    <NavigationContainer independent={true}>
      <Tab.Navigator screenOptions={{ tabBarLabelStyle: { fontFamily: "Comfortaa" }, tabBarItemStyle: { margin: 10 } }}>
        <Tab.Screen name="menu" options={{headerShown: false}} component={MenuView} />
        <Tab.Screen name="trends" options={{headerShown: false}} component={TrendsView} />
        <Tab.Screen name="live" options={{headerShown: false}} component={LiveView} />
        <Tab.Screen name="settings" options={{headerShown: false}} component={SettingsView} />
        <Tab.Screen name="credits" options={{headerShown: false}} component={CreditsView} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
