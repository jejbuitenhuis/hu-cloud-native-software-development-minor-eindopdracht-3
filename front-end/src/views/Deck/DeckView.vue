<script setup lang="ts">
import "@shoelace-style/shoelace/dist/components/button/button";
import "@shoelace-style/shoelace/dist/components/card/card";
import "@shoelace-style/shoelace/dist/components/icon/icon";
import {useRoute} from "vue-router";
import {ref} from "vue";
import CardListPreview from "./CardListPreview.vue";
import type { PrintCard, CardData } from "@/models/cardModels";
import AddCardToDeckView from "./AddCardToDeckView.vue";
import DeckSearchView from "./DeckSearchView.vue";

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
  OracleId: "76c02534-35e3-4950-b4b3-90c679cdf6a7",
  PrintId: "c742d940-1a8d-487a-a787-2ad96a96ef1f"
}

const exampleCardData : CardData = {
cardLocation: "MAIN_DECK",
card: exampleCard 
}

const errorMesssage = ref("");
const route = useRoute();
const deck = ref<Deck | null>(null);
const loading = ref(true)

const cardsList = ref();
cardsList.value = [];
const mainDeck = ref();
mainDeck.value = [];
const sideDeck = ref();
sideDeck.value = [];
const commanders = ref();
commanders.value = [];

function sortCards() {
  // temporary solution
  // TODO: add actual sorting
  mainDeck.value = cardsList.value;
  for (let card in cardsList.value) {
      sortInCard(card);
  }
}

function displayError(message : string){
  errorMesssage.value = message;
}

async function getDeck() {
  const token = localStorage.getItem("jwtToken");

  if (!token) return;
  const response = await fetch(`/api/decks/${route.params["deck_id"]}`, {headers: {Authorization: token}});

  if (!response.ok) {
    console.error(`Failed deck fetch. Status: ${response.status}`)

    return;
  }

  deck.value = await response.json() as Deck;
  // TODO: move to getcards
  loading.value = false;
}

async function getCards() {
  const token = localStorage.getItem("jwtToken");
  if (!token) return;
  const response = await fetch(`/api/decks/${route.params["deck_id"]}/cards/`, {
    headers: {Authorization: token},
  });

  if (!response.ok) {
    console.error(`Failed to fetch cards from deck. Status: ${response.status}`)
    return;
  }

  cardsList.value = await response.json() as CardData[];
  sortCards();
}

async function getCard(cardId : string) {
  const token = localStorage.getItem("jwtToken");
  if (!token) return;
  const response = await fetch(`/api/decks/${route.params["deck_id"]}/cards/${cardId}`, {
    headers: {Authorization: token},
  });

  if (!response.ok) {
    console.error(`Failed to fetch cards from deck. Status: ${response.status}`)
    return;
  }
  console.log(await response.json() as CardData)
  return await response.json() as CardData;
}


function addCardToList(event : any) {
  console.log(event)
  getCard(event['deckCardId']).then((response) => sortInCard(response))
}

function sortInCard(card : CardData){
  switch (card['cardLocation']){
    case ('COMMANDER'):
      commanders.value.push(card);
      return;
    case ('MAIN_DECK'):
      mainDeck.value.push(card);
      return;
    case ('SIDE_DECK'):
      sideDeck.value.push(card);
      return;
  }
  console.error("Couldn't sort card with location: " + card.cardLocation + ".");
}

mainDeck.value = [exampleCardData];

getDeck();
getCards();
</script>

<template>
  <p v-if="loading" class="centered-content">Loading</p>
  <p v-if="errorMesssage.valueOf() !== ''" class="error">{{ errorMesssage.valueOf() }}</p>
  <div v-if="!loading && deck != null" class="page-content">
    <h2>Deck: {{deck.name}}</h2>
    <div class="cardList">

      <h3>Commander(s):</h3>
      <div v-for="card in commanders.valueOf()">
        <CardListPreview v-bind:card-data="card"></CardListPreview>
      </div>
      <AddCardToDeckView location="COMMANDER" class="addbox" v-on:card-added="addCardToList"></AddCardToDeckView>

      <h3>Main deck:</h3>
      <div v-for="card in mainDeck.valueOf()">
        <CardListPreview v-bind:card-data="card"></CardListPreview>
      </div>
      <AddCardToDeckView location="MAIN_DECK" class="addbox" v-on:card-added="addCardToList"></AddCardToDeckView>

      <h3>Side deck:</h3>
      <div v-for="card in sideDeck.valueOf()">
        <CardListPreview v-bind:card-data="card"></CardListPreview>
      </div>
      <AddCardToDeckView location="SIDE_DECK" class="addbox" v-on:card-added="addCardToList"></AddCardToDeckView>

    </div>
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
.card-list {
  -moz-column-count: 5;
  -moz-column-gap: 5px;
  -webkit-column-count: 5;
  -webkit-column-gap: 5px;
  column-count: 5;
  column-gap: 5px;
}

.error {
  color: red;
}

.addbox {
  width: 550px;
}
</style>

