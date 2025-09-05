// web/src/app/login/page.tsx

"use client";

import { useState } from 'react';
import { Lock, User } from 'lucide-react'; // Biblioteca de ícones (opcional, mas elegante)

export default function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        console.log("Tentativa de login com:", { username, password });
        alert(`Login com: ${username}`);
    };

    return (
        // --- Container Principal ---
        // Ocupa a tela inteira, fundo escuro e centraliza o conteúdo
        <div className="grid grid-cols-1 grid-rows-[1fr_9fr_1fr] lg:grid-cols-2 lg:grid-rows-1 bg-background min-h-[100dvh] false">

            {/* --- Card de Login --- */}
            <div className="flex flex-col justify-center text-textMain px-4 lg:px-32 lg:py-10 w-full false">

                {/* --- Cabeçalho --- */}
                <h1 className="text-3xl font-bold">
                    Login
                </h1>
                <p className="text-[var(--textSecondary)] text-lg mt-4 font-medium mb-10">Bem-vindo de volta, trader.</p>

                {/* --- Formulário --- */}
                <form onSubmit={handleSubmit} className="space-y-6">

                    {/* --- Campo de Utilizador --- */}
                    <div className="mb-4 relative">
                        <label htmlFor="username" className="block font-medium text-textSecondary mb-2">Utilizador</label>
                        <User className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Usuário"
                            className="w-full p-3 pl-10 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
                            required
                        />
                    </div>

                    {/* --- Campo de Senha --- */}
                    <div className="mb-4 relative">
                        <label htmlFor="password" className="sr-only">Senha</label>
                        <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Senha"
                            className="w-full p-3 pl-10 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
                            required
                        />
                    </div>

                    {/* --- Botão de Submissão --- */}
                    <button
                        type="submit"
                        className="w-full py-3 font-semibold text-white bg-mainColor rounded-lg hover:bg-blue-500 transition-transform transform hover:scale-105"
                    >
                        Entrar
                    </button>
                </form>
            </div>
        </div>
    );
}