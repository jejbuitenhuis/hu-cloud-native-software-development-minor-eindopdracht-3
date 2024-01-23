<script setup lang="ts">
import "@shoelace-style/shoelace/dist/components/button/button";
import "@shoelace-style/shoelace/dist/components/card/card";
import "@shoelace-style/shoelace/dist/components/icon/icon";
import {useRoute} from "vue-router";
import {ref} from "vue";
import CardListPreview from "../CardListPreview.vue";
import type { PrintCard } from "@/models/cardModels";

type Deck = {
  id: string,
  name: string,
}

const exampleCard : PrintCard = {
  PK: "testpk",
  SK: "testsk",
  OracleName: "Goblin Commando",
  Price: 0.05,
  ReleasedAt: "2020",
  SetName: "Jumpstart",
  Rarity: "uncommon",
  CardFaces: [{
      Colors: ["R"],
      FaceName: "Goblin Commando",
      FlavorText: "With a commando around, somebody’s gonna get hurt.",
      ImageUrl: "https://cards.scryfall.io/png/front/c/7/c742d940-1a8d-487a-a787-2ad96a96ef1f.png?1601077766",
      ManaCost: "{4}{R}",
      OracleText: "When Goblin Commando enters the battlefield, it deals 2 damage to target creature.",
      TypeLine: "Creature — Goblin",
    },
    {
      Colors: ["R"],
      FaceName: "BLOKSFDJL",
      FlavorText: "test face.",
      ImageUrl: "https://mir-s3-cdn-cf.behance.net/project_modules/disp/8e427328807052.56053ef96e121.jpg",
      ManaCost: "{1}{G}",
      OracleText: "test face.",
      TypeLine: "Creature — Dog",
    }],
  OracleId: "",
  PrintId: ""
}

const route = useRoute();
const deck = ref<Deck | null>(null);
const loading = ref(true)

async function getDeck() {
  const token = localStorage.getItem("jwtToken");
  if (!token) return;
  const response = await fetch(`/api/decks/${route.params["deck_id"]}`, {headers: {Authorization: token}});
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
    <CardListPreview :card="exampleCard"></CardListPreview>
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

