<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

import "@shoelace-style/shoelace/dist/components/button/button";
import "@shoelace-style/shoelace/dist/components/card/card";
import "@shoelace-style/shoelace/dist/components/icon/icon";

const router = useRouter();

// temporary
const decks = ref<{ id: string }[]>([]);

function createDeck(): void {
  void router.push("/decks/new/");
}
</script>

<template>
  <div class="header">
    <h2>My decks</h2>

    <sl-button @click="createDeck()" data-test-id="create-deck">
      <sl-icon slot="prefix" name="plus" />

      New deck
    </sl-button>
  </div>

  <div class="deck-list">
    <sl-card
      v-for="deck in decks"
      :key="deck.id"
    >
      Deck id: {{ deck.id }}
    </sl-card>
  </div>
</template>

<style scoped lang="scss">
div.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 2em;

  h1 {
    margin: 0;
  }
}
</style>

