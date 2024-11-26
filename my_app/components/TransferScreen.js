import React, { useState } from "react";
import { View, StyleSheet } from "react-native";
import {
    Text,
    TextInput,
    Button,
    Card,
    Menu,
    Divider,
} from "react-native-paper";

export default function TransferScreen({ navigation }) {
    const [accountNumber, setAccountNumber] = useState("");
    const [bank, setBank] = useState("Chọn ngân hàng");
    const [recipientName, setRecipientName] = useState("");
    const [amount, setAmount] = useState("");
    const [menuVisible, setMenuVisible] = useState(false);

    const banks = [
        { label: "Vietcombank", value: "Vietcombank" },
        { label: "Techcombank", value: "Techcombank" },
        { label: "VietinBank", value: "VietinBank" },
        { label: "BIDV", value: "BIDV" },
        { label: "Agribank", value: "Agribank" },
        { label: "MB Bank", value: "MB Bank" },
        { label: "ACB", value: "ACB" },
        { label: "Sacombank", value: "Sacombank" },
        { label: "VPBank", value: "VPBank" },
        { label: "SHB", value: "SHB" },
    ];

    const transfer = () => {
        if (accountNumber && bank && recipientName && amount) {
            if (parseFloat(amount) >= 10000000) {
                navigation.navigate("Liveness");
            } else {
                alert(
                    `Chuyển thành công ${amount} đến ${recipientName} tại ${bank}`
                );
            }
        } else {
            alert("Vui lòng nhập đầy đủ thông tin");
        }
    };

    const logout = () => {
        navigation.navigate("Login");
    };

    return (
        <View style={styles.container}>
            <Card style={styles.card}>
                <Card.Title title="Chuyển tiền" />
                <Card.Content>
                    <TextInput
                        label="Số tài khoản"
                        value={accountNumber}
                        onChangeText={setAccountNumber}
                        style={styles.input}
                        keyboardType="numeric"
                    />
                    <Text style={styles.label}>Chọn ngân hàng</Text>
                    <Menu
                        visible={menuVisible}
                        onDismiss={() => setMenuVisible(false)}
                        anchor={
                            <Button
                                mode="outlined"
                                onPress={() => setMenuVisible(true)}
                                style={styles.menuButton}
                            >
                                {bank}
                            </Button>
                        }
                    >
                        {banks.map((b) => (
                            <Menu.Item
                                key={b.value}
                                onPress={() => {
                                    setBank(b.label);
                                    setMenuVisible(false);
                                }}
                                title={b.label}
                            />
                        ))}
                    </Menu>
                    <TextInput
                        label="Tên người nhận"
                        value={recipientName}
                        onChangeText={setRecipientName}
                        style={styles.input}
                    />
                    <TextInput
                        label="Số tiền"
                        keyboardType="numeric"
                        value={amount}
                        onChangeText={setAmount}
                        style={styles.input}
                    />
                    <Button
                        mode="contained"
                        onPress={transfer}
                        style={styles.button}
                    >
                        Chuyển tiền
                    </Button>
                    <Divider style={{ marginVertical: 10 }} />
                    <Button
                        mode="outlined"
                        onPress={logout}
                        style={styles.button}
                    >
                        Đăng xuất
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
    label: { fontSize: 16, fontWeight: "bold", marginBottom: 8 },
    menuButton: { marginBottom: 16 },
});
