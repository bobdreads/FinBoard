// src/app/login/page.tsx
"use client"

import AuthLayout from "@/components/auth/AuthLayout"
import { useForm } from "react-hook-form"

export default function LoginPage() {
    const { register, handleSubmit } = useForm()

    const onSubmit = (data: any) => {
        console.log(data)
    }

    return (
        <AuthLayout>
            <div className="mb-10">
                <h1 className="text-3xl font-bold text-textMain">Login</h1>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {/* Email */}
                <div>
                    <label htmlFor="email" className="block text-sm mb-2 text-textSecondary">
                        Email
                    </label>
                    <input
                        id="email"
                        type="email"
                        {...register("email")}
                        className="w-full rounded-md border border-componentBg bg-componentBg px-4 py-2 text-textMain focus:outline-none focus:ring-2 focus:ring-mainColor"
                        placeholder="Digite seu email"
                    />
                </div>

                {/* Senha */}
                <div>
                    <label htmlFor="password" className="block text-sm mb-2 text-textSecondary">
                        Senha
                    </label>
                    <input
                        id="password"
                        type="password"
                        {...register("password")}
                        className="w-full rounded-md border border-componentBg bg-componentBg px-4 py-2 text-textMain focus:outline-none focus:ring-2 focus:ring-mainColor"
                        placeholder="Digite sua senha"
                    />
                </div>

                {/* Esqueci a senha */}
                <div className="flex justify-end">
                    <a href="#" className="text-sm  text-white hover:underline">
                        Esqueci minha senha
                    </a>
                </div>

                {/* Botão Entrar */}
                <button
                    type="submit"
                    className="w-full py-2 rounded-md font-semibold text-white bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 hover:opacity-90"
                >
                    Entrar
                </button>

                {/* Criar conta */}
                <div className="text-center mt-4">
                    <a href="#" className="text-sm text-textSecondary hover:underline">
                        Ainda não tenho uma conta
                    </a>
                </div>
            </form>

            {/* Rodapé */}
            <footer className="text-xs text-textSecondary mt-10 text-center">
                2025 | Desenvolvido por <a href="#" className="underline">Maurício Filho</a>
            </footer>
        </AuthLayout>
    )
}
