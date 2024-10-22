import { defineConfig } from 'vite'
import path from "path"
import react from '@vitejs/plugin-react-swc';


export default defineConfig({
  plugins: [react()],
  server: {
    origin: "http://localhost:5001"
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    manifest: true,
    outDir: '../static',
    emptyOutDir: false,
    rollupOptions: {
      input: {
        main: './src/main.tsx',
      },
      output: {
        entryFileNames: 'react-components.js',
        format: 'esm',
      },
    },
  },
})
