// App.js
import React from "react";
import { Provider as PaperProvider } from "react-native-paper";
import AppNavigator from "./navigation/AppNavigator"; // Đảm bảo đường dẫn này là đúng

export default function App() {
    return (
        <PaperProvider>
            <AppNavigator />
        </PaperProvider>
    );
}
