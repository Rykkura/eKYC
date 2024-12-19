// // components/RegisterScreen.js
// import React, { useState } from "react";
// import { View, StyleSheet } from "react-native";
// import { TextInput, Button, Card } from "react-native-paper";
// import axios from "axios";
// import { AuthProvider } from "./Context.js";

// const API_URL = "http://192.168.0.104:8000/register"; // Cập nhật địa chỉ của API

// export default function RegisterScreen({ navigation }) {
//     const [username, setUsername] = useState("");
//     const [password, setPassword] = useState("");
//     const [fullname, setFullName] = useState(""); // Trường họ và tên
//     const [cccd, setCCCD] = useState("");
//     const [email, setEmail] = useState(""); // Trường email

//     const register = async () => {
//         try {
//             const response = await axios.post(API_URL, {
//                 username,
//                 password,
//                 fullname,
//                 cccd,
//                 email,
//             });
//             alert(response.data.message || "Đăng ký thành công");
//             navigation.navigate("Login");
//         } catch (error) {
//             console.error("Register error:", error);
//             alert(error.response?.data?.message || "Lỗi hệ thống");
//         }
//     };

//     return (
//         <View style={styles.container}>
//             <Card style={styles.card}>
//                 <Card.Title title="Đăng ký" />
//                 <Card.Content>
//                     <TextInput
//                         label="Họ và tên"
//                         value={fullname}
//                         onChangeText={setFullName}
//                         style={styles.input}
//                     />
//                     <TextInput
//                         label="Số CCCD"
//                         value={cccd}
//                         onChangeText={setCCCD}
//                         keyboardType="phone-pad"
//                         style={styles.input}
//                     />
//                     <TextInput
//                         label="Email"
//                         value={email}
//                         onChangeText={setEmail}
//                         keyboardType="email-address"
//                         style={styles.input}
//                     />
//                     <TextInput
//                         label="Tên đăng nhập"
//                         value={username}
//                         onChangeText={setUsername}
//                         style={styles.input}
//                     />
//                     <TextInput
//                         label="Mật khẩu"
//                         secureTextEntry
//                         value={password}
//                         onChangeText={setPassword}
//                         style={styles.input}
//                     />
//                     <Button
//                         mode="contained"
//                         onPress={() => navigation.navigate("OCRRegister")}
//                         style={styles.button}
//                     >
//                         Đăng ký
//                     </Button>
                    
//                 </Card.Content>
//             </Card>
//         </View>
//     );
// }

// const styles = StyleSheet.create({
//     container: { flex: 1, justifyContent: "center", padding: 16 },
//     card: { padding: 16 },
//     input: { marginBottom: 16 },
//     button: { marginTop: 10 },
// });


import React, { useState } from "react";
import { View, StyleSheet } from "react-native";
import { TextInput, Button, Card } from "react-native-paper";
import axios from "axios";
import { useAuth } from "../Context"; // Import Context

const API_URL = "http://192.168.0.102:8000/register";

export default function RegisterScreen({ navigation }) {
    const { authData, setAuthData } = useAuth(); // Sử dụng Context

    const register = async () => {
        try {
            const response = await axios.post(API_URL, { ...authData });
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
                        label="Họ và tên"
                        value={authData.fullname}
                        onChangeText={(value) =>
                            setAuthData({ ...authData, fullname: value })
                        }
                        style={styles.input}
                    />
                    <TextInput
                        label="Số CCCD"
                        value={authData.cccd}
                        onChangeText={(value) =>
                            setAuthData({ ...authData, cccd: value })
                        }
                        keyboardType="phone-pad"
                        style={styles.input}
                    />
                    <TextInput
                        label="Email"
                        value={authData.email}
                        onChangeText={(value) =>
                            setAuthData({ ...authData, email: value })
                        }
                        keyboardType="email-address"
                        style={styles.input}
                    />
                    <TextInput
                        label="Tên đăng nhập"
                        value={authData.username}
                        onChangeText={(value) =>
                            setAuthData({ ...authData, username: value })
                        }
                        style={styles.input}
                    />
                    <TextInput
                        label="Mật khẩu"
                        secureTextEntry
                        value={authData.password}
                        onChangeText={(value) =>
                            setAuthData({ ...authData, password: value })
                        }
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

