import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from './screens/HomeScreen';
import MemoryScreen from './screens/MemoryResponse';
import InventoryScreen from './screens/Inventory';
import ProphecyLogScreen from './screens/ProphecyLog';
import SniperTab from './screens/SniperTab';

const Tab = createBottomTabNavigator();
export default function Navigation() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarStyle: { backgroundColor: '#111', paddingBottom: 4 },
        tabBarActiveTintColor: '#0f0',
      }}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Memory" component={MemoryScreen} />
      <Tab.Screen name="Inventory" component={InventoryScreen} />
      <Tab.Screen name="ProphecyLog" component={ProphecyLogScreen} />
      <Tab.Screen name="Sniper" component={SniperTab} />
    </Tab.Navigator>
  );
}
