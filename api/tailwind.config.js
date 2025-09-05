/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/**/*.html',
    './**/static/**/*.js',
  ],
  theme: {
    extend: {
      colors:{
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
  plugins: [
    require('@tailwindcss/forms'), 
  ],
}

