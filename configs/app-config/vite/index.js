
import { defineConfig } from 'vite';

export default defineConfig({
	clearScreen: false,
	plugins: [
        // add plugins here
	],
	css: {
		modules: {
			localsConvention: 'camelCaseOnly'
		}
	},
	root: 'src',
	build: {
		outDir: '../dist',
		assetsDir: '.'
	}
});