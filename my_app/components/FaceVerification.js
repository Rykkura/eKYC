import { CameraView, CameraType, useCameraPermissions } from "expo-camera";
import { useEffect, useRef, useState } from "react";
import {
    Button,
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
    Alert,
} from "react-native";
import * as FileSystem from "expo-file-system";
import axios from "axios";

const API_URL = "https://tall-hornets-sin.loca.lt/detect_faces"; // Update this to your face recognition API URL

export default function FaceVerification({ navigation }) {
    const [facing, setFacing] = useState("front");
    const [permission, requestPermission] = useCameraPermissions();
    const [cameraRef, setCameraRef] = useState(null);
    const [waitingForResponse, setWaitingForResponse] = useState(false);

    useEffect(() => {
        if (permission && permission.granted) {
            console.log("Camera permission granted");
        }
    }, [permission]);

    const captureAndSendImage = async () => {
        if (cameraRef) {
            try {
                setWaitingForResponse(true);

                // Take photo and convert to base64
                const photo = await cameraRef.takePictureAsync();
                const base64 = await FileSystem.readAsStringAsync(photo.uri, {
                    encoding: FileSystem.EncodingType.Base64,
                });

                // Send the base64 image to the face recognition API
                const response = await axios.post(`${API_URL}`, {
                    image1: base64,
                });

                const result = response.data.result;

                if (result === "Same person") {
                    Alert.alert("Thành công");
                    navigation.navigate("Liveness");
                } else {
                    Alert.alert("Thất bại");
                }
            } catch (error) {
                console.error(error.response.data);
                Alert.alert("Đảm bảo khuôn mặt nằm trong khung hình");
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
                    We need your permission to show the camera
                </Text>
                <Button onPress={requestPermission} title="Grant Permission" />
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <CameraView
                style={styles.camera}
                facing={facing}
                ref={(ref) => setCameraRef(ref)}
            />
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
    },
    camera: {
        width: 300,
        height: 400,
        borderRadius: 250,
        overflow: "hidden",
        marginVertical: 20,
    },
    captureButton: {
        backgroundColor: "#007AFF",
        paddingVertical: 12,
        paddingHorizontal: 20,
        borderRadius: 8,
        alignItems: "center",
        width: 150,
        marginVertical: 20,
    },
    buttonText: {
        color: "#fff",
        fontSize: 18,
        fontWeight: "bold",
    },
});
