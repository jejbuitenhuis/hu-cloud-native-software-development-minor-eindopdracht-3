<script setup lang="ts">
import "@shoelace-style/shoelace/dist/components/card/card";
import {ref} from "vue";
import type {PrintCard} from "@/models/cardModels";

type Collection = {
  [key: string]: PrintCard[],
}

const collection = ref<Collection>({});
const collectionFilterQuery = ref<string>("");
const collectionOffsetPK = ref<string | null>(null);
const collectionOffsetSK = ref<string | null>(null);
const collectionLoading = ref<boolean>(true);

function constructGetCollectionUrl() {
  let url = "/api/collections";
  if (collectionFilterQuery.value != "") {
    url += `?q=${encodeURIComponent(collectionFilterQuery.value)}`
  }
  if (collectionOffsetPK.value != null && collectionOffsetSK.value != null) {
     url += collectionFilterQuery.value === "" ? "?" : "&";
     url += `pk-last-evaluated=${encodeURIComponent(collectionOffsetPK.value)}&sk-last-evaluated=${encodeURIComponent(collectionOffsetSK.value)}`
  }
  return url;
}

async function getCollection() {
  const token = localStorage.getItem("jwtToken");
  if (!token) return;

  collectionOffsetPK.value = null;
  collectionOffsetSK.value = null;

  const response = await fetch(constructGetCollectionUrl(), { headers: { Authorization: token } });
  if (!response.ok) {
    console.error(`Failed collections fetch. Status: ${response.status}`)
    return;
  }
  const body = await response.json() as any;
  const data = body["Items"] as PrintCard[];
  const newCollection: Collection = {};

  for (const instanceCard of data) {
    if (instanceCard.OracleId in newCollection) {
      newCollection[instanceCard.OracleId].push(instanceCard)
      continue;
    }
    newCollection[instanceCard.OracleId] = [instanceCard]
  }

  collectionOffsetPK.value = body["pk-last-evaluated"]
  collectionOffsetSK.value = body["sk-last-evaluated"]
  collection.value = newCollection;
  collectionLoading.value = false;
}
getCollection();

async function loadMoreFromCollection() {
  const token = localStorage.getItem("jwtToken");
  if (!token) return;

  if (collectionOffsetPK.value == null || collectionOffsetSK.value == null) return;

  const response = await fetch(constructGetCollectionUrl(), {
    headers: { Authorization: token },
  });
  if (!response.ok) {
    console.error(`Failed collections fetch. Status: ${response.status}`)
    return;
  }
  const body = await response.json() as any;
  const data = body["Items"] as PrintCard[];

  for (const instanceCard of data) {
    if (instanceCard.OracleId in collection.value) {
      collection.value[instanceCard.OracleId].push(instanceCard)
      continue;
    }
    collection.value[instanceCard.OracleId] = [instanceCard]
  }

  collectionOffsetPK.value = body["pk-last-evaluated"]
  collectionOffsetSK.value = body["sk-last-evaluated"]
  collectionLoading.value = false;
}
</script>

<template>
  <div class="collection-wrapper">
    <div class="search-collection-input-wrapper">
      <sl-input label="Filter collection" v-model="collectionFilterQuery" />
      <sl-button @click="getCollection">Filter</sl-button>
    </div>

    <p v-if="Object.keys(collection).length === 0 && !collectionLoading" class="centered-content">
      Your collection is empty.
    </p>

    <p v-if="collectionLoading" class="centered-content">
      Loading
    </p>

    <section class="cards-container">
      <sl-card v-for="(card, _) in collection" class="card">
        <img slot="image" :src="card[0].CardFaces[0].ImageUrl" alt="MTG - Card face">
        <div>Instances: {{card.length}}</div>
      </sl-card>
    </section>
    <sl-button class="load-more-button" @click="loadMoreFromCollection" :disabled="collectionOffsetPK == null || collectionOffsetSK == null">Load more</sl-button>
  </div>
</template>

<style scoped lang="scss">
.collection-wrapper {
    display: flex;
    padding-top: 1rem;
    flex-direction: column;
}
.search-collection-input-wrapper {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 0.2rem;
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
.load-more-button {
  margin: 0 2rem 2rem 2rem;
}
</style>
