import type { Metadata } from "next";
import nextFont from "next/font/local";
import "./../styles/globals.css";
import './../styles/colors.css'

const gilroy = nextFont({
  src: [
    {
      path: '../fonts/Gilroy-Regular.ttf',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../fonts/Gilroy-SemiBold.ttf',
      weight: '600',
      style: 'normal',
    },
    {
      path: '../fonts/Gilroy-ExtraBold.ttf',
      weight: '800',
      style: 'normal',
    },
  ],
  // Damos um nome à variável da fonte para usar no CSS
  variable: '--font-gilroy',
});

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
    // 3. Aplicamos a classe da fonte e a variável ao HTML
    <html lang="pt-BR" className={`${gilroy.variable} dark`}>
      <body>{children}</body>
    </html>
  );
}
