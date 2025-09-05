'use client'

import { signIn } from 'next-auth/react'
import { useState } from 'react'

export default function LoginPage() {
    // 2. Criamos "estados" para guardar o que o utilizador digita
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    // 3. Esta função será chamada quando o formulário for submetido
    const handleSubmit = (event: React.FormEvent) => {
        // Previne o comportamento padrão do formulário, que é recarregar a página
        event.preventDefault();

        console.log("Tentativa de login com:", { username, password });

        // TODO: Aqui virá a lógica para chamar a API
        alert(`Login com: ${username}`);
    };

    return (
        <div className="flex items-center justify-center min-h-screen">
            <form
                onSubmit={handleSubmit}
                className="p-8 rounded-lg shadow-lg w-full max-w-sm" // Estilo base, fique à vontade para mudar
            >
                <h2 className="text-2xl font-bold mb-6">Login</h2>

                <div className="mb-4">
                    <label htmlFor="username">Utilizador</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        // Cada vez que o utilizador digita, atualizamos o estado 'username'
                        onChange={(e) => setUsername(e.target.value)}
                        className="w-full p-2 mt-1" // Estilo base
                        required
                    />
                </div>

                <div className="mb-6">
                    <label htmlFor="password">Senha</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        // Cada vez que o utilizador digita, atualizamos o estado 'password'
                        onChange={(e) => setPassword(e.target.value)}
                        className="w-full p-2 mt-1" // Estilo base
                        required
                    />
                </div>

                <button
                    type="submit"
                    className="w-full py-2 rounded" // Estilo base
                >
                    Entrar
                </button>
            </form>
        </div>
    );
}
