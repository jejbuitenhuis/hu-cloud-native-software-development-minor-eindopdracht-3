<script setup lang="ts">
import { ref } from "vue";
import "@shoelace-style/shoelace/dist/components/input/input";
import "@shoelace-style/shoelace/dist/components/button/button";
import Title from "@/components/Title.vue";

const test = ref("");

function click(): void {

  alert(`Mooie knop: ${test.value}`);
}
</script>

<template>
  <Title />

  <sl-input maxlength="255" label="Test value" v-model="test" data-test-id="input" />

  <sl-button @click="click()">Mooie knop</sl-button>

  <p data-test-id="something"><strong>Output:</strong> {{ test }}</p>

  <p>Hi!</p>
</template>

<style scoped lang="scss">
#HomeView {
	text-align: center;
}
</style>
