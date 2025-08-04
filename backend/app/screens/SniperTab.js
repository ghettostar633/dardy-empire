import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Dimensions } from 'react-native';
import { LineChart } from 'react-native-chart-kit';

export default function SniperTab() {
  const [logs, setLogs] = useState([]);
  const [labels, setLabels] = useState([]);
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchLogs = async () => {
    try {
      const res = await fetch('http://<YOUR_BACKEND_IP>:8008/logs');
      const json = await res.json();
      setLogs(json);
      const lbs = json.map(item => item.timestamp.slice(8));
      const vals = json.map(item => {
        let v = item.payout.replace('Won','').replace('$','').trim();
        return parseFloat(v) || 0;
      });
      setLabels(lbs.reverse());
      setData(vals.reverse());
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <View className="flex-1 bg-black p-4">
      <Text className="text-2xl text-green-400 mb-4">Sniper Stats</Text>
      {data.length > 0 && (
        <LineChart
          data={{ labels, datasets: [{ data }] }}
          width={Dimensions.get('window').width - 32}
          height={220}
          chartConfig={{
            backgroundColor: '#000',
            backgroundGradientFrom: '#111',
            backgroundGradientTo: '#111',
            decimalPlaces: 2,
            color: (opacity = 1) => `rgba(0, 255, 136, ${opacity})`,
            labelColor: (opacity = 1) => `rgba(0, 255, 136, ${opacity})`,
            propsForDots: { r: '4' },
          }}
          style={{ borderRadius: 16, marginBottom: 16 }}
        />
      )}
      <FlatList
        data={logs}
        keyExtractor={item => item.timestamp}
        renderItem={({ item }) => (
          <View className="mb-2 p-2 bg-gray-800 rounded-lg">
            <Text className="text-green-300">Time: {item.timestamp}</Text>
            <Text className="text-white">Payout: {item.payout}</Text>
          </View>
        )}
      />
    </View>
  );
}
