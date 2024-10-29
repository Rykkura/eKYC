// components/RegisterScreen.js
import React, { useState } from "react";
import { View, StyleSheet } from "react-native";
import { TextInput, Button, Card } from "react-native-paper";
import axios from "axios";

const API_URL = "http://192.168.0.210:5000/register"; // Cập nhật địa chỉ của API

export default function RegisterScreen({ navigation }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const register = async () => {
        try {
            const response = await axios.post(API_URL, {
                username,
                password,
            });
            alert(response.data.message || "Đăng ký thành công");
            navigation.navigate("Login");
        } catch (error) {
            console.error("Register error:", error);
            alert(error.response?.data?.message || "Lỗi hệ thống");
        }
    };

    return (
        <View style={styles.container}>
            <Card style={styles.card}>
                <Card.Title title="Đăng ký" />
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
                        onPress={register}
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
