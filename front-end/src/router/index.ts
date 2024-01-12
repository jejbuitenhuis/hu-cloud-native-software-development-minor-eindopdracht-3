import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import RegisterView from "../views/RegisterView.vue";
import SearchView from "../views/SearchView.vue";
import CardDetailView from "../views/CardDetailView.vue";
import LoginView from "../views/LoginView.vue";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
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
			path: "/search",
			name: "search",
			component: SearchView,
		},
		{
			path: "/cards/:cardName",
			name: "cards",
			component: CardDetailView
		},	
		{	path: "/login",
			name: "login",
			component: LoginView,
		}
	],
});

export default router;
