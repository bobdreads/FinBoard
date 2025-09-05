// web/src/app/page.tsx

// 1. ATUALIZAMOS a interface para corresponder aos dados da nova API
interface Operation {
  id: number;
  asset_ticker: string;
  status: string;
  financial_result: string | null; // Pode ser nulo se a operação estiver aberta
  strategy_name: string;
  start_date: string;
}

// 2. A função de busca de dados permanece a mesma
async function getOperations(): Promise<Operation[]> {
  try {
    const response = await fetch('http://127.0.0.1:8000/dashboard/api/operations/', {
      cache: 'no-store', 
    });

    if (!response.ok) {
      throw new Error('Falha ao buscar dados da API');
    }

    const data = await response.json();
    console.log("Dados recebidos da API:", data); // Adicionámos um log para ver os dados no terminal do Next.js
    return data;

  } catch (error) {
    console.error("Erro na API:", error);
    return [];
  }
}

// 3. ATUALIZAMOS o componente para usar os novos nomes dos campos
export default async function Home() {
  const operations = await getOperations();

  return (
    <main className="container mx-auto p-8 bg-gray-900 text-white min-h-screen">
      <h1 className="text-4xl font-bold mb-6 text-cyan-400">Minhas Operações</h1>
      
      <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
        <ul className="divide-y divide-gray-700">
          
          {/* Cabeçalho da Tabela */}
          <li className="py-2 flex justify-between items-center font-bold text-gray-400 px-4">
            <span className="w-1/4">Ativo</span>
            <span className="w-1/4">Estratégia</span>
            <span className="w-1/4 text-center">Status</span>
            <span className="w-1/4 text-right">Resultado</span>
          </li>

          {operations.length === 0 && (
            <li className="py-4 text-center text-gray-500">
              Nenhuma operação encontrada.
            </li>
          )}

          {/* 4. Mapeamos as operações usando os nomes corretos: asset_ticker, financial_result, etc. */}
          {operations.map((op) => (
            <li key={op.id} className="py-4 px-4 flex justify-between items-center hover:bg-gray-700/50 rounded transition-colors">
              <div className="w-1/4">
                <p className="font-semibold text-lg">{op.asset_ticker}</p>
                <p className="text-sm text-gray-400">
                  Início: {new Date(op.start_date).toLocaleDateString()}
                </p>
              </div>
              <div className="w-1/4">
                <p className="text-gray-300">{op.strategy_name}</p>
              </div>
              <div className="w-1/4 text-center">
                <span className={`px-2 py-1 text-xs font-bold rounded-full ${
                  op.status === 'FECHADA' ? 'bg-blue-500/20 text-blue-300' : 'bg-yellow-500/20 text-yellow-300'
                }`}>
                  {op.status}
                </span>
              </div>
              <div className={`w-1/4 text-right font-bold text-lg ${
                !op.financial_result || parseFloat(op.financial_result) === 0 ? 'text-gray-400' :
                parseFloat(op.financial_result) > 0 ? 'text-green-400' : 'text-red-400'
              }`}>
                {op.financial_result ? `R$ ${parseFloat(op.financial_result).toFixed(2)}` : 'Em aberto'}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}