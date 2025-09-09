// web/src/services/apiClient.ts
import { refreshToken as refreshAuthToken } from './authService';

const API_URL = 'http://127.0.0.1:8000';

const apiClient = async (endpoint: string, options: RequestInit = {}) => {
    let accessToken = localStorage.getItem('accessToken') || sessionStorage.getItem('accessToken');

    // Função interna para fazer o fetch com o token atual
    const performFetch = async (token: string | null) => {
        const defaultHeaders: HeadersInit = {
            'Content-Type': 'application/json',
        };
        if (token) {
            defaultHeaders['Authorization'] = `Bearer ${token}`;
        }
        const config: RequestInit = {
            ...options,
            headers: { ...defaultHeaders, ...options.headers },
        };
        return fetch(`${API_URL}${endpoint}`, config);
    };

    let response = await performFetch(accessToken);

    // 1. Verificamos se o erro foi 401 (Unauthorized)
    if (response.status === 401) {
        const refreshToken = localStorage.getItem('refreshToken');

        if (refreshToken) {
            try {
                console.log('Access token expirado. A tentar renovar...');
                // 2. Tentamos obter um novo access token
                const newTokens = await refreshAuthToken(refreshToken);

                // 3. Guardamos o novo token e atualizamos a nossa variável local
                localStorage.setItem('accessToken', newTokens.access);
                accessToken = newTokens.access;

                console.log('Token renovado com sucesso. A tentar o pedido original novamente...');
                // 4. Tentamos fazer o pedido original novamente com o novo token
                response = await performFetch(accessToken);

            } catch (refreshError) {
                console.error('Falha ao renovar o token:', refreshError);
                // Se a renovação falhar, limpamos os tokens e forçamos o logout
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');
                // Redireciona para o login (isto recarrega a página)
                window.location.href = '/login';
                throw new Error('A sua sessão expirou.');
            }
        }
    }

    // O resto da lógica para tratar a resposta final
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Erro na API: ${response.statusText}`);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
};

export default apiClient;