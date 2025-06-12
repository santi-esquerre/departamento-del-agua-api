import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import fs from 'fs'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // map `@/some/path` → `<project-root>/frontend/src/some/path`
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    https: {
      key: fs.readFileSync(path.resolve(__dirname, '../certs/key.pem')),
      cert: fs.readFileSync(path.resolve(__dirname, '../certs/cert.pem')),
    },
    proxy: {
      '/api': {
        target: 'https://localhost/api',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
