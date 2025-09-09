"use client";
import { useState } from "react";
import { ChevronDown, Plus, Link as LinkIcon, LogOut, User, Settings } from "lucide-react";

export default function Header() {
    const [menuOpen, setMenuOpen] = useState(false);

    return (
        <header>
            <div className="flex items-center h-[60px] lg:h-[70px] border-b border-componentBg px-5 bg-background lg:pr-0">
                {/* Logo e botão menu */}
                <div className="flex gap-3 items-center flex-1">
                    <button className="rounded p-1.5 flex items-center justify-center text-textSecondary">
                        {/* Ícone hamburger */}
                        <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="1.5">
                            <path d="M3 7H21" strokeLinecap="round" />
                            <path d="M3 12H15" strokeLinecap="round" />
                            <path d="M3 17H21" strokeLinecap="round" />
                        </svg>
                    </button>
                    <div className="flex items-center space-x-3">
                        <img src="/assets/images/logo.svg" className="w-[28px] h-[28px]" alt="logo" />
                        <span className="text-white font-Gilroy font-bold text-2xl">FinBoard</span>
                    </div>
                </div>

                {/* Botões da direita */}
                <div className="flex gap-4 items-center h-full">
                    {/* Botão Add Trade */}
                    <button className="group flex items-center justify-center bg-mainColor text-white rounded-lg font-bold w-[35px] h-[35px] hover:w-auto hover:px-4 transition-all">
                        <span className="min-w-3">
                            <Plus size={20} />
                        </span>
                        <span className="w-0 overflow-hidden group-hover:w-auto group-hover:ml-2 transition-all whitespace-nowrap">
                            Add Trade
                        </span>
                    </button>

                    {/* Botão Broker Connection */}
                    <button className="group flex items-center justify-center bg-componentBg text-textMain rounded-lg font-bold w-[35px] h-[35px] hover:w-auto hover:px-4 transition-all">
                        <span className="min-w-3">
                            <LinkIcon size={20} />
                        </span>
                        <span className="w-0 overflow-hidden group-hover:w-auto group-hover:ml-2 transition-all whitespace-nowrap">
                            Broker Connection
                        </span>
                    </button>

                    {/* Divisor */}
                    <div className="bg-thirdDark h-6 w-[1px]"></div>

                    {/* Dropdown do usuário */}
                    <div className="relative h-full">
                        <button
                            type="button"
                            className="hidden lg:flex items-center gap-3 px-6 cursor-pointer hover:bg-componentBg h-full min-w-[280px] max-w-[320px]"
                            onClick={() => setMenuOpen(!menuOpen)}
                        >
                            <div className="truncate flex-1">
                                <div className="font-bold text-textMain truncate">zezinho@gmail.com</div>
                                <div><span className="font-medium text-sm text-textSecondary">FinBoard Pro</span></div>
                            </div>
                            <ChevronDown className={`transition-transform ${menuOpen ? "rotate-180" : ""}`} />
                        </button>

                        {menuOpen && (
                            <div className="absolute top-full right-0 w-[320px] bg-componentBg rounded-b-lg shadow-lg overflow-hidden z-10">
                                <a href="#" className="flex items-center gap-4 hover:bg-thirdDark text-textMain py-3 px-4">
                                    <User size={20} className="text-textSecondary" /> Meu Perfil
                                </a>
                                <a href="#" className="flex items-center gap-4 hover:bg-thirdDark text-textMain py-3 px-4">
                                    <Settings size={20} className="text-textSecondary" /> Configurações
                                </a>
                                <div className="border-t border-thirdDark my-2"></div>
                                <a href="#" className="flex items-center gap-4 hover:bg-thirdDark text-red-500 py-3 px-4">
                                    <LogOut size={20} /> Sair
                                </a>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </header>
    );
}
