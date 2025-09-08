// web/src/context/AuthContext.tsx
"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';
// Renomeei o import para evitar conflito de nomes, uma boa prática.
import { loginUser as apiLogin } from '@/services/authService';

// 1. Definimos a "forma" do nosso contexto com os tipos corretos
interface AuthContextType {
    isAuthenticated: boolean;
    // AQUI: Adicionamos os tipos para username e password
    login: (username: string, password: string) => Promise<void>;
    logout: () => void;
    isLoading: boolean;
}

// 2. Criamos o Contexto com um valor padrão
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// 3. Criamos o Provedor (AuthProvider), o nosso gestor de estado
export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        console.log("Verificando sessão existente...");
        setIsAuthenticated(false);
        setIsLoading(false);
    }, []);

    // AQUI: Adicionamos os tipos aos parâmetros da função
    const login = async (username: string, password: string) => {
        const data = await apiLogin(username, password);
        console.log("Tokens recebidos:", data);

        localStorage.setItem('accessToken', data.access);
        localStorage.setItem('refreshToken', data.refresh);

        setIsAuthenticated(true);
    };

    const logout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
};

// 4. O nosso Hook customizado (sem alterações)
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth deve ser usado dentro de um AuthProvider');
    }
    return context;
};