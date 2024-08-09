import { defineConfig } from 'vite';
import { nodePolyfills } from 'vite-plugin-node-polyfills';


// Export the Vite configuration
export default defineConfig({
  plugins: [
    // Node polyfills to support Node.js built-in modules
    nodePolyfills(),
  ],
  optimizeDeps: {
    // Exclude specific packages or files from Vite's dependency optimization
    exclude: ['@mapbox/node-pre-gyp']
  },
  build: {
    rollupOptions: {
      external: ['@mapbox/node-pre-gyp']
    }
  }
});

