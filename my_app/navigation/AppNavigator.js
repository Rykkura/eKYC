import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';
import LoginScreen from '../components/LoginScreen';
import RegisterScreen from '../components/RegisterScreen';
import TransferScreen from '../components/TransferScreen';
import LivenessDetectionApp from '../components/LivenessDetectionApp'; // Import màn hình liveness

const Stack = createStackNavigator();

function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} options={{ title: 'Đăng nhập' }} />
        <Stack.Screen name="Register" component={RegisterScreen} options={{ title: 'Đăng ký' }} />
        <Stack.Screen name="Transfer" component={TransferScreen} options={{ title: 'Chuyển tiền' }} />
        <Stack.Screen name="Liveness" component={LivenessDetectionApp} options={{ title: 'Kiểm tra Liveness' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default AppNavigator;
