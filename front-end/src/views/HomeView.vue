<template>
	<h1>Hello, World!</h1>

	<sl-input maxlength="255" label="Test value" v-model="test" />

	<sl-button @click="click()">Mooie knop</sl-button>

	<p><strong>Output:</strong> {{ test }}</p>
</template>

<script setup lang="ts">
import { ref } from "vue";
import "@shoelace-style/shoelace/dist/components/input/input";
import "@shoelace-style/shoelace/dist/components/button/button";

const test = ref("");

function click(): void {
	alert(`Mooie knop: ${test.value}`);
}
</script>

<style scoped lang="scss">
#HomeView {
	text-align: center;
}
</style>
