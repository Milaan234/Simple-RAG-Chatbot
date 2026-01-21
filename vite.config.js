import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // This rule tells Vite: 
      // "If you see a request starting with /recommend, send it to Flask on port 5000"
      '/askAI': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false,
      },
    }
  }
})
