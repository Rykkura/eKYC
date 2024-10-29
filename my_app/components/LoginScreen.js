// components/LoginScreen.js
import React, { useState } from "react";
import { View, StyleSheet } from "react-native";
import { TextInput, Button, Card } from "react-native-paper";
import axios from "axios"; // Thêm axios để gửi yêu cầu HTTP

const API_URL = "http://192.168.0.210:5000/login"; // Địa chỉ API của bạn (thay bằng địa chỉ IP nếu trên thiết bị thực)

export default function LoginScreen({ navigation }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const login = async () => {
        try {
            const response = await axios.post(`${API_URL}`, {
                username,
                password,
            });

            // Nếu không cần token, bạn có thể bỏ qua dòng này
            // const { token } = response.data;

            // Điều hướng đến màn hình chuyển tiền
            navigation.navigate("Transfer");
        } catch (error) {
            alert(error.response?.data?.message || "Lỗi hệ thống"); // Hiển thị thông báo lỗi
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
                        onPress={() => navigation.navigate("Register")}
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
