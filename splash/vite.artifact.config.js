import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: 'dist-artifact',
    minify: false,
    rollupOptions: {
      output: {
        manualChunks(id) { if (id.includes('node_modules')) return 'vendor' },
        entryFileNames: 'assets/app.js', chunkFileNames: 'assets/[name].js', assetFileNames: 'assets/[name][extname]',
      },
    },
  },
})
