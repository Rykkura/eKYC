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

const API_URL = " http://192.168.0.104:5000/liveness_detection"; // Địa chỉ API Flask của bạn
const questions = ["smile", "turn face right", "turn face left"];

export default function LivenessDetectionApp({ navigation }) {
    const [facing, setFacing] = useState("front");
    const [permission, requestPermission] = useCameraPermissions();
    const [cameraRef, setCameraRef] = useState(null);
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const questionPool = useRef([...questions]); // Dùng để lưu mảng câu hỏi có thể thay đổi
    const [waitingForResponse, setWaitingForResponse] = useState(false);

    useEffect(() => {
        if (permission && permission.granted) {
            displayRandomQuestion();
        }
    }, [permission]);

    useEffect(() => {
        if (currentQuestion && !waitingForResponse) {
            const timeout = setTimeout(() => {
                captureAndSendImage();
            }, 5000); // 5 giây sau khi hiện câu hỏi

            return () => clearTimeout(timeout);
        }
    }, [currentQuestion, waitingForResponse]);

    const displayRandomQuestion = () => {
        if (questionPool.current.length === 0) {
            questionPool.current = [...questions];
        }

        const randomIndex = Math.floor(
            Math.random() * questionPool.current.length
        );
        const nextQuestion = questionPool.current[randomIndex];
        setCurrentQuestion(nextQuestion);
        questionPool.current.splice(randomIndex, 1);
    };

    const captureAndSendImage = async () => {
        if (cameraRef) {
            try {
                setWaitingForResponse(true);

                const photo = await cameraRef.takePictureAsync();
                const base64 = await FileSystem.readAsStringAsync(photo.uri, {
                    encoding: FileSystem.EncodingType.Base64,
                });

                const response = await axios.post(`${API_URL}`, {
                    image: base64,
                    question: currentQuestion,
                });

                const result = response.data.result;

                if (result === "pass") {
                    Alert.alert("Kết quả phát hiện sống", "Pass");
                    displayRandomQuestion(); // Chuyển sang câu hỏi mới nếu pass
                } else {
                    Alert.alert("Kết quả phát hiện sống", "Fail");
                    setTimeout(captureAndSendImage, 5000);
                }
            } catch (error) {
                Alert.alert("Lỗi", "Không thể bắt đầu phát hiện sống.");
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
            <CameraView
                style={styles.camera}
                facing={facing}
                ref={(ref) => setCameraRef(ref)}
            >
                <View style={styles.questionContainer}>
                    <Text style={styles.questionText}>{currentQuestion}</Text>
                </View>
            </CameraView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: "center",
    },
    message: {
        textAlign: "center",
        paddingBottom: 10,
    },
    camera: {
        flex: 1,
    },
    questionContainer: {
        position: "absolute",
        top: 50,
        alignSelf: "center",
        backgroundColor: "rgba(0, 0, 0, 0.6)",
        padding: 10,
        borderRadius: 5,
    },
    questionText: {
        color: "white",
        fontSize: 24,
        fontWeight: "bold",
    },
});
