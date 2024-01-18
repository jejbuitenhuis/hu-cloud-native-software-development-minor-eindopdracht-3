<script setup lang="ts">
import "@shoelace-style/shoelace/dist/components/card/card";
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
type CombinedCardInstance = CardInstanceCard & {
  FrontFace: CardInstanceFace,
  BackFace: CardInstanceFace | undefined,
}
type Collection = {
  [key: string]: CombinedCardInstance[],
}

const collection = ref<Collection>({});
const collectionLoading = ref<boolean>(true);

async function getCollection() {
  const token = localStorage.getItem("jwtToken");
  if (!token) return;
  const response = await fetch("/api/collections", {headers: {Authorization: token}});
  if (!response.ok) {
    console.error(`Failed collections fetch. Status: ${response.status}`)
    return;
  }
  const data = await response.json() as CardInstance[];
  const newCollection: Collection = {};
  const instanceCards = data.filter(v => v.DataType == "Card") as CardInstanceCard[];
  const instanceFaces = data.filter(v => v.DataType == "Face") as CardInstanceFace[];

  for (const instanceCard of instanceCards) {
    const frontFace = instanceFaces.find(v => v.FaceType === "Front" && v.CardInstanceId === instanceCard.CardInstanceId) as CardInstanceFace;
    const backFace = instanceFaces.find(v => v.FaceType === "Back" && v.CardInstanceId === instanceCard.CardInstanceId);

    const newInstance: CombinedCardInstance = {
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
  collection.value = newCollection;
  collectionLoading.value = false;
}
getCollection();
</script>

<template>
  <div class="collection-wrapper">
    <section class="cards-container">
      <p v-if="Object.keys(collection).length === 0 && !collectionLoading">
        Your collection is empty.
      </p>
      <p v-if="collectionLoading">
        Loading
      </p>

      <!--TODO: Replace with card component-->
      <sl-card v-for="(card, _) in collection" class="card">
        <img slot="image" :src="card[0]['FrontFace']['ImageLink']" alt="MTG - Card face">
        <div>Instances: {{card.length}}</div>
      </sl-card>
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
  width: 15rem;
  img {
    height: inherit;
    border-radius: 1rem;
  }
}
</style>
