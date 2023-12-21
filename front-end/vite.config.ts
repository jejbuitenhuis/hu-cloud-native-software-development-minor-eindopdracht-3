import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
	server: {
		port: 8080,
	},
	plugins: [
		vue({
			template: {
				compilerOptions: {
					isCustomElement: tag => tag.startsWith("sl-"),
				},
			},
		}),
	],
	resolve: {
		alias: {
			"@": fileURLToPath(
				new URL("./src", import.meta.url),
			),
		},
	},
});
