import { CameraView, useCameraPermissions } from "expo-camera";
import { useState } from "react";
import {
    Button,
    StyleSheet,
    Text,
    View,
    Alert,
    TouchableOpacity,
    TextInput,
} from "react-native";
import * as FileSystem from "expo-file-system";
import axios from "axios";

const API_URL = "http://192.168.0.104:5000/ocr";

export default function OCR({ navigation }) {
    const [permission, requestPermission] = useCameraPermissions();
    const [cameraRef, setCameraRef] = useState(null);
    const [waitingForResponse, setWaitingForResponse] = useState(false);
    

    const captureAndSendImage = async () => {
        if (cameraRef) {
            try {
                setWaitingForResponse(true);

                const photo = await cameraRef.takePictureAsync();
                const base64 = await FileSystem.readAsStringAsync(photo.uri, {
                    encoding: FileSystem.EncodingType.Base64,
                });

                // Gửi ảnh đến API
                const response = await axios.post(`${API_URL}`, {
                    image1: base64,
                });

                const data = response.data;
                
                // Lấy các giá trị từ API và cập nhật vào các trường tương ứng
                navigation.navigate("OCRInfo", {
                    cccd: data.CCCD ? data.CCCD[0] : "",
                    hoTen: data.ho_ten ? data.ho_ten[0] : "",
                    ngaySinh: data.ngay_sinh ? data.ngay_sinh[0] : "",
                    queQuan: data.que_quan ? data.que_quan[0] : "",
                });

                Alert.alert("Kết quả", "Ảnh đã được gửi thành công!");
            } catch (error) {
                console.error(error);
                Alert.alert("Lỗi", "Không thể chụp ảnh và gửi đến API.");
            } finally {
                setWaitingForResponse(false);
            }
        }
    };

    if (!permission) {
        return <View />;
    }

    if (!permission.granted) {
        return (
            <View style={styles.container}>
                <Text style={styles.message}>
                    Chúng tôi cần quyền của bạn để hiển thị camera
                </Text>
                <Button onPress={requestPermission} title="Cấp quyền" />
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <View style={styles.cameraContainer}>
                <CameraView
                    style={styles.camera}
                    ref={(ref) => setCameraRef(ref)}
                />
            </View>
            <TouchableOpacity
                style={styles.captureButton}
                onPress={captureAndSendImage}
                disabled={waitingForResponse}
            >
                <Text style={styles.buttonText}>Chụp</Text>
            </TouchableOpacity>

        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#f0f0f0",
    },
    cameraContainer: {
        width: 400,
        height: 300,
        overflow: "hidden",
        borderRadius: 20,
        borderWidth: 2,
        borderColor: "#ccc",
        marginBottom: 20,
    },
    camera: {
        flex: 1,
    },
    captureButton: {
        backgroundColor: "#007AFF",
        paddingVertical: 12,
        paddingHorizontal: 20,
        borderRadius: 8,
        alignItems: "center",
        width: 200,
        marginBottom: 20,
    },
    buttonText: {
        color: "#fff",
        fontSize: 18,
        fontWeight: "bold",
    },
    inputContainer: {
        width: "80%",
    },
    input: {
        height: 40,
        borderColor: "#ccc",
        borderWidth: 1,
        borderRadius: 5,
        marginBottom: 10,
        paddingHorizontal: 10,
    },
});
