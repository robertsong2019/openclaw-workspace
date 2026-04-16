/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'trust-high': '#3fb950',
        'trust-medium': '#d29922',
        'trust-low': '#f85149',
        'behavior-cooperative': '#3fb950',
        'behavior-neutral': '#d29922',
        'behavior-malicious': '#f85149',
        'behavior-adversarial': '#bc8cff',
      },
    },
  },
  plugins: [],
}
