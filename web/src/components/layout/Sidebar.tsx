"use client";
import Link from "next/link";
import { LayoutDashboard, Notebook, Briefcase } from "lucide-react";
import { usePathname } from "next/navigation";

const menu = [
    { label: "Dashboard", href: "/dashboard/overview", icon: LayoutDashboard },
    { label: "Journal", href: "/journal/notes", icon: Notebook },
    { label: "Portfolios", href: "/portfolios/create", icon: Briefcase },
];

export default function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="bg-background w-[250px] min-h-full border-r border-componentBg flex flex-col p-5 gap-5">
            {menu.map(({ label, href, icon: Icon }) => (
                <Link
                    key={href}
                    href={href}
                    className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors 
            ${pathname.startsWith(href) ? "bg-mainColor text-white" : "text-textMain hover:bg-thirdDark"}`}
                >
                    <Icon size={18} />
                    {label}
                </Link>
            ))}
        </aside>
    );
}
