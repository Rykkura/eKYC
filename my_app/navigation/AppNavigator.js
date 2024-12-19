import React from "react";
import { createStackNavigator } from "@react-navigation/stack";
import { NavigationContainer } from "@react-navigation/native";
import LoginScreen from "../components/LoginScreen";
import RegisterScreen from "../components/RegisterScreen";
import Register from "../components/Register/Register";

import TransferScreen from "../components/Login/TransferScreen";
import LivenessDetectionApp from "../components/Login/LivenessDetectionApp"; // Import màn hình liveness
import LivenessDetectionRegister from "../components/Register/LivenessDetectionRegister"; // Import màn hình liveness

import OCR from "../components/Login/OCR";
import OCRRegister from "../components/Register/OCRRegister";
import OCRInfo from "../components/Login/OCR_Info";
import OCRInfoRegister from "../components/Register/OCRInfoRegister";
import FaceVerification from "../components/Login/FaceVerification";
import FaceVerificationRegister from "../components/Register/FaceVerificationRegister";

const Stack = createStackNavigator();

function AppNavigator() {
    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="Login">
                <Stack.Screen
                    name="Login"
                    component={LoginScreen}
                    options={{ title: "Đăng nhập" }}
                />
                <Stack.Screen
                    name="RegisterScreen"
                    component={RegisterScreen}
                    options={{ title: "Đăng ký" }}
                />
                <Stack.Screen
                    name="Register"
                    component={Register}
                    options={{ title: "Đăng ký" }}
                />
                <Stack.Screen
                    name="Transfer"
                    component={TransferScreen}
                    options={{ title: "Chuyển tiền" }}
                />
                <Stack.Screen
                    name="Liveness"
                    component={LivenessDetectionApp}
                    options={{ title: "Kiểm tra Liveness" }}
                />
                <Stack.Screen
                    name="LivenessRegister"
                    component={LivenessDetectionRegister}
                    options={{ title: "Kiểm tra Liveness" }}
                />
                <Stack.Screen
                    name="OCR"
                    component={OCR}
                    options={{ title: "Kiểm tra CCCD" }}
                />
                <Stack.Screen
                    name="OCRRegister"
                    component={OCRRegister}
                    options={{ title: "Kiểm tra CCCD" }}
                />
                <Stack.Screen
                    name="OCRInfo"
                    component={OCRInfo}
                    options={{ title: "Thông tin CCCD" }}
                />
                <Stack.Screen
                    name="OCRInfoRegister"
                    component={OCRInfoRegister}
                    options={{ title: "Thông tin CCCD" }}
                />
                <Stack.Screen
                    name="FaceVerification"
                    component={FaceVerification}
                    options={{ title: "Xác thực khuôn mặt" }}
                />
                <Stack.Screen
                    name="FaceVerificationRegister"
                    component={FaceVerificationRegister}
                    options={{ title: "Xác thực khuôn mặt" }}
                />
            </Stack.Navigator>
        </NavigationContainer>
    );
}

export default AppNavigator;
