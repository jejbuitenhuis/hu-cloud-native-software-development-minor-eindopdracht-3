import "@shoelace-style/shoelace/dist/themes/light.css";
import { setBasePath } from "@shoelace-style/shoelace";

setBasePath("https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.12.0/cdn/");

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

createApp(App)
	.use(createPinia())
	.use(router)
	.mount("#app");
