// App.js
import React from "react";
import { Provider as PaperProvider } from "react-native-paper";
import AppNavigator from "./navigation/AppNavigator"; // Đảm bảo đường dẫn này là đúng
import { AuthProvider } from "./components/Context.js";
export default function App() {
    return (
        <AuthProvider>
            <PaperProvider>
                <AppNavigator />
            </PaperProvider>
        </AuthProvider>
    );
}
