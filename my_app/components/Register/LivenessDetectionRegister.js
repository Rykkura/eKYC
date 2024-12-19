import React, { useEffect, useRef, useState } from "react";
import { Camera, CameraView } from "expo-camera";
import {
    Button,
    StyleSheet,
    Text,
    View,
    Alert,
    Dimensions,
    TouchableOpacity,
} from "react-native";
import axios from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";
const API_URL = "https://78bb-213-173-108-101.ngrok-free.app/upload"; // API Flask của bạn
const questions = ["smile", "turn face right", "turn face left", "blink eyes"];

export default function LivenessDetectionRegister({ navigation }) {
    const [cameraPermission, setCameraPermission] = useState(null);
    const [audioPermission, setAudioPermission] = useState(null);
    const cameraRef = useRef(null);
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const questionPool = useRef([...questions]);
    const [isRecording, setIsRecording] = useState(false);
    const [videoUri, setVideoUri] = useState(null);
    var count = 0;
    var result = 'pass';
    useEffect(() => {
        (async () => {
            const cameraStatus = await Camera.requestCameraPermissionsAsync();
            const audioStatus =
                await Camera.requestMicrophonePermissionsAsync();
            setCameraPermission(cameraStatus.status === "granted");
            setAudioPermission(audioStatus.status === "granted");

            if (
                cameraStatus.status === "granted" &&
                audioStatus.status === "granted"
            ) {
                displayRandomQuestion();
            }
        })();
    }, []);

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
        // setTimeout(() => {
        //     startOrStopVideoRecording();
        // }, 2000);
    };

    const recordVideo = async () => {
        if (cameraRef.current) {
            try {
                setIsRecording(true);
                const video = await cameraRef.current.recordAsync({
                    quality: "1080p",
                    maxDuration: 3,
                });
                setVideoUri(video.uri);
                setIsRecording(false);
                console.log("Video recording completed", video.uri);
                return video.uri;
            } catch (error) {
                setIsRecording(false);
                console.error("Error recording video:", error);
                Alert.alert("Lỗi", "Không thể quay video.");
            }
        }
    };

    const stopVideoRecording = async () => {
        if (cameraRef.current && isRecording) {
            cameraRef.current.stopRecording();
            setIsRecording(false);
        }
    };

    const startOrStopVideoRecording = async () => {
        if (isRecording) {
            stopVideoRecording();
        } else {
            const videoPath = await recordVideo();
            if (videoPath) {
                uploadVideo(videoPath);
            }
        }
    };

    const uploadVideo = async (videoPath) => {
        try {
            const formData = new FormData();
            formData.append("video", {
                uri: videoPath,
                name: "video.mp4",
                type: "video/mp4",
            });
            formData.append("question", currentQuestion);
            const response = await axios.post(API_URL, formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            // var result = response.data.result;
            console.log("Result:", result);
            
            Alert.alert(result === "pass" ? "Thành công" : "Thử lại");

            if (result === "pass") {
                count++;
                console.log(count);
                if (count === 3) {
                    navigation.navigate("Register");
                } else {
                    displayRandomQuestion();
                    startOrStopVideoRecording();
                }
            } else {
                setTimeout(() => {
                    startOrStopVideoRecording();
                }, 3000);
            }
        } catch (error) {
            console.error("Error uploading video:", error);
            Alert.alert("Lỗi", "Không thể gửi video lên server.");
        }
    };

    if (!cameraPermission || !audioPermission) {
        return (
            <View style={styles.container}>
                <Text style={styles.message}>
                    Chúng tôi cần quyền để truy cập camera và micro
                </Text>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <CameraView
                style={styles.camera}
                facing="front"
                ref={cameraRef}
                mode="video"
            >
                <View style={styles.questionContainer}>
                    <Text style={styles.questionText}>{currentQuestion}</Text>
                </View>
                <Button
                    title={isRecording ? "Đang quay video" : ""}
                    onPress={startOrStopVideoRecording}
                />
                <TouchableOpacity
                    style={styles.captureButton}
                    onPress={startOrStopVideoRecording}
                >
                    <Text style={styles.buttonText}>Bắt đầu xác minh</Text>
                </TouchableOpacity>
            </CameraView>
        </View>
    );
}

const WINDOW_HEIGHT = Dimensions.get("window").height;
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
    captureButton: {
        backgroundColor: "#007AFF",
        paddingVertical: 12,
        paddingHorizontal: 20,
        borderRadius: 8,
        alignItems: "center",
        width: 200,
        position: "absolute", // Add this line for absolute positioning
        bottom: 20, // Adjust to your preference for vertical positioning
        left: "50%", // Centers the button horizontally
        marginLeft: -100, // Half the width of the button (200px/2) to center it perfectly
    },
    buttonText: {
        color: "#fff",
        fontSize: 18,
        fontWeight: "bold",
    },
});
