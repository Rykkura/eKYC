import { CameraView, useCameraPermissions } from "expo-camera";
import { useState, useEffect } from "react";
import {
    Button,
    StyleSheet,
    Text,
    View,
    Alert,
    TouchableOpacity,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import * as FileSystem from "expo-file-system";
import axios from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";

const API_URL = "https://78bb-213-173-108-101.ngrok-free.app/ocr";

export default function OCR({ navigation }) {
    const [permission, requestPermission] = useCameraPermissions();
    const [cameraRef, setCameraRef] = useState(null);
    const [waitingForResponse, setWaitingForResponse] = useState(false);
    const [token, setToken] = useState(null);

    useEffect(() => {
        const fetchToken = async () => {
            const storedToken = await AsyncStorage.getItem("jwtToken");
            setToken(storedToken);
        };
        fetchToken();
    }, []);

    const captureAndSendImage = async () => {
        if (cameraRef) {
            try {
                setWaitingForResponse(true);
                const photo = await cameraRef.takePictureAsync();
                const base64 = await FileSystem.readAsStringAsync(photo.uri, {
                    encoding: FileSystem.EncodingType.Base64,
                });
                await sendImageToAPI(base64);
            } catch (error) {
                console.error(error);
                Alert.alert("Lỗi", "Không thể chụp ảnh và gửi đến API.");
            } finally {
                setWaitingForResponse(false);
            }
        }
    };

    const pickImageFromLibrary = async () => {
        try {
            const result = await ImagePicker.launchImageLibraryAsync({
                mediaTypes: ImagePicker.MediaTypeOptions.Images,
                allowsEditing: true,
                base64: true,
                quality: 1,
            });

            if (!result.canceled && result.assets.length > 0) {
                const base64 = result.assets[0].base64;
                setWaitingForResponse(true);
                await sendImageToAPI(base64);
            }
        } catch (error) {
            console.error(error);
            Alert.alert("Lỗi", "Không thể chọn ảnh từ thư viện.");
        } finally {
            setWaitingForResponse(false);
        }
    };

    const sendImageToAPI = async (base64) => {
        try {
            const response = await axios.post(
                `${API_URL}`,
                {
                    image1: base64,
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            const data = response.data;
            navigation.navigate("OCRInfoRegister", {
                cccd: data.CCCD ? data.CCCD[0] : "",
                hoTen: data.ho_ten ? data.ho_ten[0] : "",
                ngaySinh: data.ngay_sinh ? data.ngay_sinh[0] : "",
                queQuan: data.que_quan ? data.que_quan[0] : "",
            });

            
        } catch (error) {
            console.error(error);
            Alert.alert("Lỗi", "Không thể tải ảnh.");
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
            <TouchableOpacity
                style={[styles.captureButton, styles.uploadButton]}
                onPress={pickImageFromLibrary}
                disabled={waitingForResponse}
            >
                <Text style={styles.buttonText}>Chọn ảnh</Text>
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
        marginBottom: 10,
    },
    uploadButton: {
        backgroundColor: "#34C759",
        alignItems: "center",
    },
    buttonText: {
        color: "#fff",
        fontSize: 18,
        fontWeight: "bold",
    },
});
