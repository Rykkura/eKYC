import { useState } from "react";
import { StyleSheet, View, Text } from "react-native";
import { TextInput, Button, Card } from "react-native-paper";

export default function OCRInfo({ navigation, route }) {
    const { cccd, hoTen, ngaySinh, queQuan } = route.params;
    const [cccdValue, setCCCD] = useState(cccd);
    const [hoTenValue, setHoTen] = useState(hoTen);
    const [ngaySinhValue, setNgaySinh] = useState(ngaySinh);
    const [queQuanValue, setQueQuan] = useState(queQuan);
    return (
        <View style={styles.container}>
            <Text>CCCD:</Text>
            <TextInput
                style={styles.input}
                value={cccdValue}
                onChangeText={setCCCD}
            />
            <Text>Họ Tên:</Text>
            <TextInput
                style={styles.input}
                value={hoTenValue}
                onChangeText={setHoTen}
            />
            <Text>Ngày Sinh:</Text>
            <TextInput
                style={styles.input}
                value={ngaySinhValue}
                onChangeText={setNgaySinh}
            />
            <Text>Quê Quán:</Text>
            <TextInput
                style={styles.input}
                value={queQuanValue}
                onChangeText={setQueQuan}
            />
            <Button
                mode="contained"
                onPress={() => navigation.navigate("FaceVerification")}
                style={styles.button}
            >
                Tiếp tục
            </Button>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        backgroundColor: "#f0f0f0",
        justifyContent: "center",
    },
    input: {
        height: 50,
        borderColor: "#ccc",
        borderWidth: 1,
        borderRadius: 5,
        marginBottom: 10,
        paddingHorizontal: 10,
    },
    button: {
        backgroundColor: "#007AFF",
        paddingVertical: 12,
        paddingHorizontal: 20,
        borderRadius: 8,
        alignItems: "center",
        marginBottom: 20,
        marginTop: 40,
    },
});
