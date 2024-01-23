<script setup lang="ts">
import "@shoelace-style/shoelace/dist/components/button/button";
import "@shoelace-style/shoelace/dist/components/card/card";
import "@shoelace-style/shoelace/dist/components/icon/icon";
import {useRoute} from "vue-router";
import {ref} from "vue";

type Deck = {
  id: string,
  name: string,
}

const route = useRoute();
const deck = ref<Deck | null>(null);
const loading = ref(true)

async function getDeck() {
  const token = localStorage.getItem("jwtToken");

  if (!token) return;

  const response = await fetch(`/api/decks/${route.params["deck_id"]}`, { headers: { Authorization: token } });

  if (!response.ok) {
    console.error(`Failed collections fetch. Status: ${response.status}`)

    return;
  }

  deck.value = await response.json() as Deck;
  loading.value = false;
}
getDeck();
</script>

<template>
  <p v-if="loading" class="centered-content">Loading</p>

  <div v-if="!loading && deck != null" class="page-content">
    <h2>Deck: {{deck.name}}</h2>
    <p>Here will come cool cards :)</p>
  </div>
</template>

<style scoped lang="scss">
.page-content {
  margin: 2rem;
}
.centered-content {
  margin-top: 20%;
  text-align: center;
}
</style>

