import React, { useState } from "react";
import { View, StyleSheet } from "react-native";
import { TextInput, Button, Card } from "react-native-paper";
import axios from "axios";
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = "http://192.168.0.102:8000/login";

export default function LoginScreen({ navigation }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const login = async () => {
        try {
            const response = await axios.post(`${API_URL}`, {
                username,
                password,
            });
            // const { token } = response.data;
            // await AsyncStorage.setItem("token", token); 
            // Điều hướng đến màn hình kiểm tra liveness sau khi đăng nhập thành công
            navigation.navigate("Transfer");    
        } catch (error) {
            alert(error.response?.data?.message || "Lỗi hệ thống");
        }
    };

    return (
        <View style={styles.container}>
            <Card style={styles.card}>
                <Card.Title title="Đăng nhập" />
                <Card.Content>
                    <TextInput
                        label="Tên đăng nhập"
                        value={username}
                        onChangeText={setUsername}
                        style={styles.input}
                    />
                    <TextInput
                        label="Mật khẩu"
                        secureTextEntry
                        value={password}
                        onChangeText={setPassword}
                        style={styles.input}
                    />
                    <Button
                        mode="contained"
                        onPress={login}
                        style={styles.button}
                    >
                        Đăng nhập
                    </Button>
                    <Button
                        onPress={() => navigation.navigate("RegisterScreen")}
                        style={styles.button}
                    >
                        Đăng ký
                    </Button>
                </Card.Content>
            </Card>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: "center", padding: 16 },
    card: { padding: 16 },
    input: { marginBottom: 16 },
    button: { marginTop: 10 },
});
