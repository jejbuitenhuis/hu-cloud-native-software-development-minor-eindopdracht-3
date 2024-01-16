import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import RegisterView from "../views/RegisterView.vue";
import LoginView from "../views/LoginView.vue";

const router = createRouter({
	history: createWebHashHistory(),
	routes: [
		{
			path: "/",
			name: "home",
			component: HomeView,
		},
		{
			path: "/register",
			name: "register",
			component: RegisterView,
		},
		{
			path: "/login",
			name: "login",
			component: LoginView,
		},
		{
			path: "/:pathMatch(.*)*",
			name: "not-found",
			component: () => import("../views/NotFoundView.vue"),
		},
	],
});

export default router;
