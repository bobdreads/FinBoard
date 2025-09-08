// web/src/app/page.tsx
"use client";

import { useEffect, useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import apiClient from '@/services/apiClient';
import { useRouter } from 'next/navigation'; // Importamos o router para redirecionamento

// 1. Definimos a nova interface para 'Trade', baseada no nosso novo Serializer
interface Trade {
  id: number;
  symbol: string;
  side: 'BUY' | 'SELL';
  is_open: boolean;
  net_result: string;
  portfolio_name: string;
  created_at: string;
}

export default function HomePage() {
  const { isAuthenticated, isLoading: isAuthLoading } = useAuth(); // Pegamos o estado de carregamento da autenticação
  const router = useRouter();

  const [trades, setTrades] = useState<Trade[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Se a verificação de autenticação ainda está a decorrer, não fazemos nada
    if (isAuthLoading) {
      return;
    }

    // Se o utilizador não está autenticado, redireciona para o login
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    // Se está autenticado, buscamos os trades
    const fetchTrades = async () => {
      try {
        setError(null);
        setIsLoading(true);
        // 2. AQUI ESTÁ A MUDANÇA: Apontamos para o novo endpoint de trades!
        const data = await apiClient('/dashboard/api/trades/');
        setTrades(data);
      } catch (err: any) {
        setError(err.message);
        console.error("Erro ao buscar trades:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTrades();
  }, [isAuthenticated, isAuthLoading, router]); // Dependências do useEffect

  // Se a autenticação estiver a carregar, mostramos uma mensagem genérica
  if (isAuthLoading || isLoading) {
    return <p className="text-center mt-10">A carregar...</p>;
  }

  if (error) {
    return <p className="text-center mt-10 text-red-400">Erro ao carregar os dados: {error}</p>;
  }

  // O seu JSX para renderizar a lista de trades
  return (
    <main className="container mx-auto p-8">
      <h1 className="text-4xl font-bold mb-6">Meus Trades</h1>

      {trades.length === 0 ? (
        <p>Nenhum trade encontrado. Adicione um através do painel de administração do Django para começar.</p>
      ) : (
        <ul>
          {/* 3. Mapeamos os trades e usamos os novos campos */}
          {trades.map(trade => (
            <li key={trade.id} className="border-b border-gray-700 py-2">
              <p className="font-bold">{trade.symbol} - <span className={trade.side === 'BUY' ? 'text-green-400' : 'text-red-400'}>{trade.side}</span></p>
              <p className="text-sm text-gray-400">Resultado: R$ {parseFloat(trade.net_result).toFixed(2)}</p>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}