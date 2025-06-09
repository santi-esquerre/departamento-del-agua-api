import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    https: {
      key: fs.readFileSync('/certs/key.pem'),
      cert: fs.readFileSync('/certs/cert.pem'),
    },
    port: 443,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://web:8000',
        changeOrigin: true,
      },
    },
  },
})
