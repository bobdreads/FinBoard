// web/src/services/authService.ts

// A URL base da nossa API Django.
// É uma boa prática defini-la num só lugar.
const API_URL = 'http://127.0.0.1:8000';

// 1. Definimos uma interface para o que a função de login vai retornar.
//    Isto ajuda na auto-completação e na verificação de tipos noutras partes do código.
interface TokenResponse {
    access: string;
    refresh: string;
}

/**
 * Tenta autenticar um utilizador na API.
 * @param username O nome de utilizador.
 * @param password A senha.
 * @returns Uma promessa que resolve com os tokens de acesso e de atualização.
 */
// 2. Adicionamos os tipos aos parâmetros e ao retorno da função.
export const loginUser = async (
    username: string,
    password: string
): Promise<TokenResponse> => {
    const response = await fetch(`${API_URL}/api/token/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Falha na autenticação');
    }

    const data: TokenResponse = await response.json();
    return data;
};

/**
 * Usa o refresh token para obter um novo access token.
 * @param refresh O refresh token guardado.
 * @returns Uma promessa que resolve com o novo access token.
 */
export const refreshToken = async (refresh: string) => {
    const response = await fetch(`${API_URL}/api/token/refresh/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh }),
    });

    if (!response.ok) {
        // Se o refresh token também falhar, o utilizador precisa de fazer login novamente.
        throw new Error('Sessão expirada. Por favor, faça login novamente.');
    }

    const data = await response.json();
    return data; // Deve conter um novo 'access' token
};

// TODO: No futuro, adicionaremos aqui as funções registerUser, refreshToken, etc.