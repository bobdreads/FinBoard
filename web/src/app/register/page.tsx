"use client";

import AuthLayout from "@/components/auth/AuthLayout";

export default function RegisterPage() {
    return (
        <AuthLayout>
            <div className="mb-10">
                <h1 className="text-3xl font-semibold text-textMain">Criar Conta</h1>
            </div>
            <form className="space-y-6">
                <div>
                    <label htmlFor="nome" className="block text-sm mb-2 text-textSecondary">
                        Nome
                    </label>
                    <input
                        id="nome"
                        type="nome"
                        className="w-full rounded-md border border-componentBg bg-componentBg px-4 py-2 text-textMain focus:outline-none focus:ring-2 focus:ring-mainColor"
                        placeholder="Digite seu Nome"
                    />
                </div>
                <div>
                    <label htmlFor="email" className="block text-sm mb-2 text-textSecondary">
                        Email
                    </label>
                    <input
                        id="email"
                        type="email"
                        className="w-full rounded-md border border-componentBg bg-componentBg px-4 py-2 text-textMain focus:outline-none focus:ring-2 focus:ring-mainColor"
                        placeholder="Digite seu email"
                    />
                </div>
                <div>
                    <label htmlFor="password" className="block text-sm mb-2 text-textSecondary">
                        Senha
                    </label>
                    <input
                        id="password"
                        type="password"
                        className="w-full rounded-md border border-componentBg bg-componentBg px-4 py-2 text-textMain focus:outline-none focus:ring-2 focus:ring-mainColor"
                        placeholder="Digite sua senha"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full py-2 mt-6 rounded-md font-semibold text-white bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 hover:opacity-90"
                >
                    Criar Conta
                </button>

                <div className="mt-4 text-center text-sm text-textSecondary">
                    Já tem uma conta? <a href="/login" className="text-blue-400  hover:underline">Entrar!</a>
                </div>
            </form>

            {/* Rodapé */}
            <footer className="text-xs text-textSecondary mt-10 text-center">
                2025 | Desenvolvido por <a href="#" className="underline">Maurício Filho</a>
            </footer>

        </AuthLayout>
    );
}
