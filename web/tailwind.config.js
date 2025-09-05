/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
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
        Gilroy: ['Gilroy', 'sans-serif'],
      }
    },
  },
  plugins: [],
}


