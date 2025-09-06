import type { Metadata } from "next";
import "./../styles/globals.css";



export const metadata: Metadata = {
  title: "FinBoard",
  description: "Sua plataforma de gestão de trades.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // Aplicamos 'dark' para o tema escuro do Tailwind funcionar
    <html lang="pt-BR" className="dark">
      <body>{children}</body>
    </html>
  );
}
