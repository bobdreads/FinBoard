"use client";

import AuthLayout from "@/components/auth/AuthLayout";

export default function ForgotPasswordPage() {
    return (
        <AuthLayout>
            <div className="mb-10">
                <h1 className="text-3xl font-semibold text-textMain">Recuperar Senha</h1>
            </div>
            <form className="space-y-6">
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
                <button
                    type="submit"
                    className="w-full py-2 mt-4 rounded-md font-semibold text-white bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 hover:opacity-90"
                >
                    Enviar link de recuperação
                </button>
                <div className="mt-4 text-center">
                    <a href="/login" className="text-sm text-textSecondary hover:underline">
                        Voltar para o login
                    </a>
                </div>
            </form>

            {/* Rodapé */}
            <footer className="text-xs text-textSecondary mt-10 text-center">
                2025 | Desenvolvido por <a href="#" className="underline">Maurício Filho</a>
            </footer>

        </AuthLayout>
    );
}
