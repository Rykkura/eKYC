import React, { createContext, useState, useContext } from "react";

const Context = createContext();

export const AuthProvider = ({ children }) => {
    const [authData, setAuthData] = useState({
        username: "",
        password: "",
        fullname: "",
        cccd: "",
        email: "",
    });

    return (
        <Context.Provider value={{ authData, setAuthData }}>
            {children}
        </Context.Provider>
    );
};

export const useAuth = () => useContext(Context);