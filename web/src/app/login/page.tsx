'use client'

import { useState } from 'react'
import { signIn } from 'next-auth/react'
import AuthLayout from '@/components/auth/AuthLayout';

export default function LoginPage() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const [errorMessage, setErrorMessage] = useState<string | null>(null)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setIsLoading(true)
        setErrorMessage(null)

        const res = await signIn('credentials', {
            redirect: false,
            email,
            password,
        })

        if (res?.error) {
            setErrorMessage('Credenciais inválidas')
        } else {
            window.location.href = '/dashboard'
        }

        setIsLoading(false)
    }

    return (
        <AuthLayout>
            <div className="flex flex-col justify-center text-textMain px-4 lg:px-32 lg:py-10 w-full false">
                <h2 className="text-3xl font-semibold text-textMain text-center mb-6">FinBoard</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-textSecondary">
                            Email
                        </label>
                        <input
                            id="email"
                            type="email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="mt-1 w-full px-4 py-2 bg-cardBackground border border-componentBg text-textMain rounded-md focus:outline-none focus:ring-2 focus:ring-mainColor"
                            placeholder="exemplo@dominio.com"
                        />
                    </div>
                    <div>
                        <label htmlFor="password" className="block text-sm font-medium text-textSecondary">
                            Senha
                        </label>
                        <input
                            id="password"
                            type="password"
                            required
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="mt-1 w-full px-4 py-2 bg-cardBackground border border-componentBg text-textMain rounded-md focus:outline-none focus:ring-2 focus:ring-mainColor"
                            placeholder="••••••••"
                        />
                    </div>

                    {errorMessage && <p className="text-sm text-mainColor">{errorMessage}</p>}

                    <button
                        type="submit"
                        className="w-full py-2 mt-4 text-white bg-mainColor font-semibold rounded-md hover:bg-thirdDark transition-colors"
                        disabled={isLoading}
                    >
                        {isLoading ? 'Carregando...' : 'Entrar'}
                    </button>
                </form>
                <div className="mt-4 text-center">
                    <a href="/auth/forgot-password" className="text-mainColor underline text-sm">
                        Esqueceu a senha?
                    </a>
                </div>
            </div>

            {/* Lado direito - imagem */}
            <div
                className="hidden lg:flex w-1/2 bg-cover bg-center"
                style={{ backgroundImage: "url('/images/login-image.jpg')" }}>
            </div>
        </AuthLayout>
    )
}
