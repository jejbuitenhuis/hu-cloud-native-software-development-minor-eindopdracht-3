<script setup lang="ts">
import "@shoelace-style/shoelace/dist/components/input/input";
import "@shoelace-style/shoelace/dist/components/button/button";
import Header from "@/components/Header.vue";
import {ref} from "vue";

type CardInstanceCard = {
  DataType: "Card",
  CardInstanceId: string,
  PrintId: string,
  DeckId: string | undefined,
}
type CardInstanceFace = {
  DataType: "Face",
  FaceType: "Front" | "Back",
  CardInstanceId: string,
  PrintId: string,
  DeckId: string | undefined,
  ImageLink: string,
}
type CardInstance = CardInstanceCard | CardInstanceFace;
type Collection = {
  [key: string]: [CardInstanceCard & {
    FrontFace: CardInstanceFace;
    BackFace: CardInstanceFace | undefined;
  }],
}

const collection = ref<Collection>({});

async function getCollection() {
  const response = await fetch("/api/collections", {headers: {Authorization: localStorage.getItem("jwtToken")}});
  if (!response.ok) {
    console.error(`Failed collections fetch. Status: ${response.status}`)
    return;
  }
  const data = await response.json() as CardInstance[];
  const newCollection: Collection = {}
  const instanceCards: CardInstanceCard[] = data.filter(v => v.DataType == "Card")
  const instanceFaces: CardInstanceFace[] = data.filter(v => v.DataType == "Face")

  for (const instanceCard of instanceCards) {
    const frontFace = instanceFaces.find(v => v.FaceType === "Front" && v.CardInstanceId === instanceCard.CardInstanceId);
    const backFace = instanceFaces.find(v => v.FaceType === "Back" && v.CardInstanceId === instanceCard.CardInstanceId);

    const newInstance = {
      ...instanceCard,
      FrontFace: frontFace,
      BackFace: backFace,
    }

    if (instanceCard.PrintId in newCollection) {
      newCollection[instanceCard.PrintId].push(newInstance)
      continue;
    }
    newCollection[instanceCard.PrintId] = [newInstance]
  }
  collection.value = newCollection
}
getCollection();
</script>

<template>
  <Header />

  <div class="collection-wrapper">
    <p v-if="collection.length > 0">
    Your collection is empty.
    </p>
    <section v-else class="cards-container">
      <!--TODO: Replace with card component-->
      <div v-for="(card, _) in collection" class="card">
        <img :src="card[0]['FrontFace']['ImageLink']" alt="MTG - Card face">
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
.collection-wrapper {
    display: flex;
    padding-top: 1rem;
    flex-direction: column;
}
.cards-container {
  display: flex;
  flex-wrap: wrap;
  padding: 1rem;
}
.card {
  margin: 1rem;
  height: 20rem;
  img {
    height: inherit;
  }
}
</style>
