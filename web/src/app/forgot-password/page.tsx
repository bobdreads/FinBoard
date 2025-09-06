"use client";

import AuthLayout from "@/components/auth/AuthLayout";

export default function ForgotPasswordPage() {
    return (
        <AuthLayout>
            <h1 className="text-3xl font-bold mb-6 text-center">Recuperar Senha</h1>
            <form className="space-y-4">
                <div>
                    <label className="block text-sm mb-1">Email cadastrado</label>
                    <input
                        type="email"
                        className="w-full rounded-lg border px-3 py-2 text-sm bg-transparent"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full py-2 rounded-lg bg-gradient-to-r from-purple-500 to-orange-400 text-white font-semibold"
                >
                    Enviar link de recuperação
                </button>
            </form>
            <div className="mt-4 text-center">
                <a href="/auth/login" className="text-sm text-blue-400">
                    Voltar para o login
                </a>
            </div>
        </AuthLayout>
    );
}
