// web/src/components/auth/AuthLayout.tsx

import React from 'react';

// O layout aceita 'children', que será o nosso formulário específico (Login, Registo, etc.)
export default function AuthLayout({ children }: { children: React.ReactNode }) {
    return (
        // --- Container Principal (A "moldura" que se repete) ---
        <section className='grid lg:grid-cols-2 bg-background min-h-[100dvh]'>
            {/* Lado esquerdo - formulário */}
            <div className="flex items-center justify-center">
                {children}
            </div>
            {/* Lado direito - imagem */}
            <div
                className="hidden lg:flex bg-cover bg-center"
                style={{ backgroundImage: "url('assets/images/login-bg.jpg')" }}
            />
        </section>
    );
}