// web/src/context/AuthContext.tsx
"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';
import { loginUser as apiLogin } from '@/services/authService';
import { refreshToken as refreshAuthToken } from '@/services/authService';

interface AuthContextType {
    isAuthenticated: boolean;
    // 1. A função de login agora aceita o parâmetro 'rememberMe'
    login: (username: string, password: string, rememberMe?: boolean) => Promise<void>;
    logout: () => void;
    isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    // Agora, este useEffect verifica a sessão de forma inteligente
    useEffect(() => {
        const initializeAuth = async () => {
            // 2. Procura o refresh token em ambos os locais, dando prioridade ao localStorage
            const refreshToken = localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken');

            if (refreshToken) {
                try {
                    console.log("Sessão encontrada, a tentar renovar o token...");
                    const newTokens = await refreshAuthToken(refreshToken);

                    // Se o refresh token estava no localStorage, mantemos a sessão persistente
                    const storage = localStorage.getItem('refreshToken') ? localStorage : sessionStorage;
                    storage.setItem('accessToken', newTokens.access);

                    setIsAuthenticated(true);
                    console.log("Sessão restaurada com sucesso.");
                } catch (error) {
                    console.error("Falha ao restaurar a sessão, a limpar tokens.", error);
                    // Limpa tokens inválidos de ambos os locais
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                    sessionStorage.removeItem('accessToken');
                    sessionStorage.removeItem('refreshToken');
                    setIsAuthenticated(false);
                }
            }
            setIsLoading(false);
        };

        initializeAuth();
    }, []);

    const login = async (username: string, password: string, rememberMe = false) => {
        const data = await apiLogin(username, password);

        // 3. Escolhe onde guardar os tokens com base na escolha do utilizador
        const storage = rememberMe ? localStorage : sessionStorage;

        console.log(`A guardar tokens no ${rememberMe ? 'localStorage' : 'sessionStorage'}.`);
        storage.setItem('accessToken', data.access);
        storage.setItem('refreshToken', data.refresh);

        setIsAuthenticated(true);
    };

    const logout = () => {
        // 4. Garante que limpamos de ambos os locais ao fazer logout
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        sessionStorage.removeItem('accessToken');
        sessionStorage.removeItem('refreshToken');
        setIsAuthenticated(false);
        // Opcional: redireciona para o login após o logout
        window.location.href = '/login';
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, logout, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth deve ser usado dentro de um AuthProvider');
    }
    return context;
};