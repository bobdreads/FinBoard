// src/app/login/page.tsx
"use client"

import AuthLayout from "@/components/auth/AuthLayout"
import { useForm } from "react-hook-form"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { loginUser } from "@/services/authService"
import { useAuth } from "@/context/AuthContext"
import { Eye, EyeOff } from "lucide-react"

export default function LoginPage() {
    const { register, handleSubmit } = useForm()
    const [error, setError] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState(false)
    const router = useRouter()
    const [showPassword, setShowPassword] = useState(false)
    const { login } = useAuth();

    // 3. A nossa lógica de submissão agora é async e usa o 'data' do react-hook-form
    const onSubmit = async (data: any) => {
        setIsLoading(true)
        setError(null)

        try {
            await login(data.username, data.password)

            // Se o login for bem-sucedido, redirecionamos para a dashboard
            router.push("/")

        } catch (err: any) {
            console.error("Erro no login:", err.message)
            setError(err.message)
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <AuthLayout>
            <div className="mb-10">
                <h1 className="text-3xl font-semibold text-textMain">Login</h1>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {/* Email */}
                <div>
                    <label htmlFor="username" className="block text-sm mb-2 text-textSecondary">
                        Usuário
                    </label>
                    <input
                        id="username"
                        type="text"
                        {...register("username")}
                        className="w-full rounded-md border border-componentBg bg-componentBg px-4 py-2 text-textMain focus:outline-none focus:ring-2 focus:ring-mainColor"
                        placeholder="Digite seu usuário"
                    />
                </div>

                {/* Senha */}
                <div>
                    <label htmlFor="password" className="block text-sm mb-2 text-textSecondary">
                        Senha
                    </label>
                    <input
                        id="password"
                        type={showPassword ? "text" : "password"}
                        {...register("password")}
                        className="w-full rounded-md border border-componentBg bg-componentBg px-4 py-2 text-textMain focus:outline-none focus:ring-2 focus:ring-mainColor"
                        placeholder="Digite sua senha"
                    />
                    <button
                        type="button" // Importante: 'type="button"' para não submeter o formulário
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-[38px] text-textSecondary hover:text-textMain"
                    >
                        {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                </div>

                {/* Esqueci a senha e manter conectado */}
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <input
                            id="rememberMe"
                            type="checkbox"
                            {...register("rememberMe")}
                            className="h-4 w-4 rounded border-gray-600 bg-gray-700 text-mainColor focus:ring-mainColor"
                        />
                        <label htmlFor="rememberMe" className="text-sm text-textSecondary">
                            Manter conectado
                        </label>
                    </div>

                    <a href="/forgot-password" className="text-sm  text-blue-400  hover:underline">
                        Esqueceu a senha?
                    </a>
                </div>

                {/* 5. Adicionamos o feedback de erro aqui */}
                {error && (
                    <p className="text-sm text-red-400 text-center">{error}</p>
                )}

                {/* Botão Entrar */}
                <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full py-2 rounded-md font-semibold text-white bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 hover:opacity-90 disabled:opacity-50"
                >
                    {isLoading ? "Entrando..." : "Entrar"}
                </button>

                {/* Criar conta */}
                <div className="text-center text-sm text-textSecondary mt-4">
                    Ainda não tem uma conta? <a href="/register" className="text-blue-400 hover:underline">Criar conta.</a>
                </div>
            </form>

            {/* Rodapé */}
            <footer className="text-xs text-textSecondary mt-10 text-center">
                2025 | Desenvolvido por <a href="#" className="underline">Maurício Filho</a>
            </footer>
        </AuthLayout>
    )
}
