import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import tailwindcss from 'tailwindcss' 

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  css : {
    postcss : {
      plugins : [
        tailwindcss(), 
      ]
    }
  },
  resolve: {
    alias: {
      '@r2d2/ui': path.resolve(__dirname, '../../../packages/ui/src'),
      '@': path.resolve(__dirname, './src')
    }
  },
})
