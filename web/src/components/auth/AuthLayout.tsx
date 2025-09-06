import { ReactNode } from "react"

export default function AuthLayout({ children }: { children: ReactNode }) {
    return (
        <section className="grid lg:grid-cols-2 bg-background min-h-screen relative">
            {/* Lado esquerdo - formulário */}
            <div className="flex items-center justify-center px-6">
                <div className="w-full max-w-md">{children}</div>
            </div>

            {/* Lado direito - imagem com overlay esfumaçado */}
            <div className="hidden lg:block relative w-full h-full">
                <div
                    className="absolute inset-0 bg-cover bg-center"
                    style={{ backgroundImage: "linear-gradient(to right, rgba(0,0,0,0.6), rgba(0,0,0,0)), url('/assets/images/login-bg.jpg')" }}
                />
                {/* Gradiente esfumaçado que "mescla" com o lado esquerdo */}
                <div className="absolute inset-0 bg-gradient-to-l from-background/95 to-transparent" />
            </div>
        </section>
    )
}