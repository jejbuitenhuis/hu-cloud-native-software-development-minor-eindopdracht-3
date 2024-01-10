import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "node:path";
import basicSsl from "@vitejs/plugin-basic-ssl";

export default defineConfig({
	server: {
		port: 8080,
		proxy: {
			'/api': {
				target : "https://d24n8wcogmyxee.cloudfront.net/",
				changeOrigin: true
			}
		}
	},
	plugins: [
		vue({
			template: {
				compilerOptions: {
					isCustomElement: (tag: any) => tag.startsWith("sl-"),

					nodeTransforms: [
						// https://github.com/vitejs/vite/issues/636#issuecomment-665545551
						(node: any) => {
							if (process.env.NODE_ENV === 'production' && node.type === 1 /* NodeTypes.ELEMENT */) {
								for (let i = 0; i < node.props.length; i++) {
									const p = node.props[i];

									if (p && p.type === 6 /* NodeTypes.ATTRIBUTE */ && p.name === "data-test-id") {
										node.props.splice(i, 1);
										i--;
									}
								}
							}
						},
					],
				},
			},
		}),
		// @ts-ignore fuck off typescript
		basicSsl()
	],
	resolve: {
		alias: {
			"@": fileURLToPath(
				new URL("./src", import.meta.url),
			),
		},
	},
});