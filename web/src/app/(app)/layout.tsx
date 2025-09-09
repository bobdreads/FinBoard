// web/src/app/(app)/layout.tsx

export default function AppLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <main>
            {/* TODO: Adicionar aqui a Sidebar e o Navbar */}
            {children}
        </main>
    );
}