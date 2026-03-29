export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        page: '#F5F5F0',
        surface: '#FFFFFF',
        'surface-secondary': '#F8F8F4',
        border: '#D8D8D0',
        'text-primary': '#1A1A1A',
        'text-secondary': '#5A5A5A',
        'text-muted': '#8A8A8A',
        accent: '#1A3A6B',
        'warn-red': '#C0392B',
        'warn-orange': '#D35400',
        'warn-yellow': '#B7950B',
      },
      fontFamily: {
        'serif': ['Crimson Text', 'serif'],
        'sans': ['IBM Plex Sans', 'sans-serif'],
        'mono': ['IBM Plex Mono', 'monospace'],
      },
      spacing: {
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px',
        '8': '32px',
      },
      fontSize: {
        'xs': '11px',
        'sm': '12px',
        'base': '14px',
        'lg': '16px',
        'xl': '22px',
      },
      borderRadius: {
        'none': '0px',
        'sm': '4px',
        'md': '6px',
        'lg': '8px',
      },
      borderWidth: {
        '1': '1px',
      },
    },
  },
  plugins: [],
}
