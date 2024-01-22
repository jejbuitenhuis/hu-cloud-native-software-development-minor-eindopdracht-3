<script setup lang="ts">
import "@shoelace-style/shoelace/dist/components/card/card";
import {ref} from "vue";
import type {CombinedPrint, PrintCard, PrintFace, PrintPart} from "@/models/cardModels";

type Collection = {
  [key: string]: CombinedPrint[],
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
  const data = await response.json() as PrintPart[];
  const newCollection: Collection = {};
  const instanceCards = data.filter(v => v.DataType == "Card") as PrintCard[];
  const instanceFaces = data.filter(v => v.DataType == "Face") as PrintFace[];

  for (const instanceCard of instanceCards) {
    const newInstance: CombinedPrint = {
      ...instanceCard,
      Faces: instanceFaces.filter(v => v.OracleId === instanceCard.PrintId)
    }

    if (instanceCard.PK in newCollection) {
      newCollection[instanceCard.PK].push(newInstance)
      continue;
    }
    newCollection[instanceCard.PK] = [newInstance]
  }
  collection.value = newCollection;
  collectionLoading.value = false;
}
getCollection();
</script>

<template>
  <div class="collection-wrapper">
    <p v-if="Object.keys(collection).length === 0 && !collectionLoading" class="centered-content">
      Your collection is empty.
    </p>

    <p v-if="collectionLoading" class="centered-content">
      Loading
    </p>

    <section class="cards-container">
      <sl-card v-for="(card, _) in collection" class="card">
        <img slot="image" :src="card[0].Faces[0].ImageUrl" alt="MTG - Card face">
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
.centered-content {
  margin-top: 20%;
  text-align: center;
}
</style>
