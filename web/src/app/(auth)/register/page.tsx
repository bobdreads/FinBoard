// web/src/app/register/page.tsx
"use client"

import AuthLayout from "@/components/auth/AuthLayout"
import { useForm } from "react-hook-form"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { registerUser } from "@/services/authService" // Importamos a função

export default function RegisterPage() {
    const { register, handleSubmit, watch, formState: { errors } } = useForm();
    const password = watch("password"); // "Espiamos" o campo da senha para o validar

    const [error, setError] = useState<string | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();

    const onSubmit = async (data: any) => {
        setIsLoading(true);
        setError(null);
        setSuccessMessage(null);

        try {
            await registerUser(data.username, data.email, data.password);
            setSuccessMessage("Conta criada com sucesso! A redirecionar para o login em 3 segundos...");

            setTimeout(() => {
                router.push("/login");
            }, 3000);

        } catch (err: any) {
            console.error("Erro no registo:", err.message);
            setError(err.message);
            setIsLoading(false);
        }
    };

    return (
        <AuthLayout>
            <div className="mb-10">
                <h1 className="text-3xl font-semibold text-textMain">Crie sua conta</h1>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                {/* Utilizador */}
                <div>
                    <label htmlFor="username" className="block text-sm mb-2 text-textSecondary">Username</label>
                    <input
                        id="username"
                        type="text"
                        {...register("username", { required: "O username é obrigatório." })}
                        className="w-full rounded-md border border-componentBg bg-componentBg px-4 py-2 text-textMain focus:outline-none focus:ring-2 focus:ring-mainColor"
                        placeholder="Digite seu username"
                    />
                    {errors.username && <p className="text-red-400 text-xs mt-1">{String(errors.username.message)}</p>}
                </div>

                {/* Email */}
                <div>
                    <label htmlFor="email" className="block text-sm mb-2 text-textSecondary">Email</label>
                    <input
                        id="email"
                        type="email"
                        {...register("email", {
                            required: "O email é obrigatório.",
                            pattern: { value: /^\S+@\S+$/i, message: "Formato de email inválido." }
                        })}
                        className="w-full rounded-md border border-componentBg bg-componentBg px-4 py-2 text-textMain focus:outline-none focus:ring-2 focus:ring-mainColor"
                        placeholder="Digite seu email"
                    />
                    {errors.email && <p className="text-red-400 text-xs mt-1">{String(errors.email.message)}</p>}
                </div>

                {/* Senha */}
                <div>
                    <label htmlFor="password" className="block text-sm mb-2 text-textSecondary">Senha</label>
                    <input
                        id="password"
                        type="password"
                        {...register("password", {
                            required: "A senha é obrigatória.",
                            minLength: { value: 8, message: "A senha deve ter no mínimo 8 caracteres." }
                        })}
                        className="w-full rounded-md border border-componentBg bg-componentBg px-4 py-2 text-textMain focus:outline-none focus:ring-2 focus:ring-mainColor"
                        placeholder="Crie uma senha forte"
                    />
                    {errors.password && <p className="text-red-400 text-xs mt-1">{String(errors.password.message)}</p>}
                </div>

                {/* Confirmar Senha */}
                <div>
                    <label htmlFor="confirmPassword" className="block text-sm mb-2 text-textSecondary">Confirme a Senha</label>
                    <input
                        id="confirmPassword"
                        type="password"
                        {...register("confirmPassword", {
                            required: "A confirmação da senha é obrigatória.",
                            validate: value => value === password || "As senhas não coincidem."
                        })}
                        className="w-full rounded-md border border-componentBg bg-componentBg px-4 py-2 text-textMain focus:outline-none focus:ring-2 focus:ring-mainColor"
                        placeholder="Digite a senha novamente"
                    />
                    {errors.confirmPassword && <p className="text-red-400 text-xs mt-1">{String(errors.confirmPassword.message)}</p>}
                </div>

                {/* Feedback de Sucesso ou Erro */}
                {error && <p className="text-sm text-red-400 text-center">{error}</p>}
                {successMessage && <p className="text-sm text-green-400 text-center">{successMessage}</p>}

                <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full py-2 mt-2 rounded-md font-semibold text-white bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 hover:opacity-90 disabled:opacity-50"
                >
                    {isLoading ? "A criar conta..." : "Criar conta"}
                </button>

                <div className="text-center text-sm text-textSecondary mt-4">
                    Já tem uma conta? <a href="/login" className="text-blue-400 hover:underline">Faça login.</a>
                </div>
            </form>

            <footer className="text-xs text-textSecondary mt-10 text-center">
                2025 | Desenvolvido por <a href="#" className="underline">Maurício Filho</a>
            </footer>
        </AuthLayout>
    )
}