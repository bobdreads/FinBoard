/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        componentBg: "var(--componentBackground)",
        background: "var(--background)",
        textMain: "var(--textMain)",
        textSecondary: "var(--textSecondary)",
        cardBackground: "var(--cardBackground)",
        mainColor: "var(--mainColor)",
        thirdDark: "var(--thirdDark)",
      },
      fontFamily: {
        sans: ['var(--font-gilroy)', 'sans-serif'],
      }
    },
  },
  plugins: [],
}


