/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{html,py}"],
  theme: {
      extend: {
          colors: {
              orange: "#FF6F00",
              dark: "#1E1E1E",
          },
          fontFamily: {
              montserrat: ["Montserrat", "sans-serif"],
          },
          boxShadow: {
              "lg-dark": "0 10px 15px -4px rgb(0 0 0 / 0.3), 0 4px 6px -5px rgb(0 0 0 / 0.3)"
          }
      },
  },
  plugins: [],
}
