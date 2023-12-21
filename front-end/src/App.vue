<template>
	<RouterView />
</template>

<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap");

html,
body {
	margin: 0;
	padding: 0;
	font-size: 16px;
	line-height: 1.6;
}

* {
	box-sizing: border-box;
	font-family: "Inter", sans-serif;
}
</style>
