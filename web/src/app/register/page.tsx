// web/src/app/register/page.tsx

"use client";
import AuthLayout from "@/components/auth/AuthLayout"; // Reutilizando!

export default function RegisterPage() {
    return (
        <AuthLayout>
            {/* TODO: Construir o formulário de registo aqui */}
            <div className="text-center">
                <h3 className="font-bold text-xl mb-4">Página de Registo</h3>
                <p className="text-gray-400">O formulário de registo virá aqui!</p>
                <button className="mt-4 w-full py-3 font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700">
                    Registrar
                </button>
            </div>
        </AuthLayout>
    )
}