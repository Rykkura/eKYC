import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useState } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View, Alert } from 'react-native';
import * as FileSystem from 'expo-file-system';
import axios from 'axios';

const API_URL = "http://192.168.0.103:5000"; // Địa chỉ API Flask của bạn

export default function App() {
  const [facing, setFacing] = useState('front'); // Khởi tạo biến facing
  const [permission, requestPermission] = useCameraPermissions();
  const [cameraRef, setCameraRef] = useState(null); // Tham chiếu đến camera

  if (!permission) {
    // Quyền camera vẫn đang được tải.
    return <View />;
  }

  if (!permission.granted) {
    // Quyền camera chưa được cấp.
    return (
      <View style={styles.container}>
        <Text style={styles.message}>Chúng tôi cần quyền của bạn để hiển thị camera</Text>
        <Button onPress={requestPermission} title="Cấp quyền" />
      </View>
    );
  }

  const startLivenessDetection = async () => {
    if (cameraRef) {
      try {
        const photo = await cameraRef.takePictureAsync();
        
        // Đọc tệp hình ảnh và chuyển đổi sang base64
        const base64 = await FileSystem.readAsStringAsync(photo.uri, {
          encoding: FileSystem.EncodingType.Base64,
        });

        // Gửi hình ảnh dưới dạng base64 tới API
        const response = await axios.post(`${API_URL}/start_liveness`, {
          image: base64,
        });

        const result = response.data.result;
        Alert.alert("Kết quả phát hiện sống", result); // Hiển thị kết quả
      } catch (error) {
        console.error(error);
        Alert.alert("Lỗi", "Không thể bắt đầu phát hiện sống.");
      }
    }
  };

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} facing={facing} ref={(ref) => setCameraRef(ref)}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.button} onPress={startLivenessDetection}>
            <Text style={styles.text}>Bắt đầu phát hiện sống</Text>
          </TouchableOpacity>
        </View>
      </CameraView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  message: {
    textAlign: 'center',
    paddingBottom: 10,
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: 'transparent',
    margin: 64,
  },
  button: {
    flex: 1,
    alignSelf: 'flex-end',
    alignItems: 'center',
  },
  text: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
});
