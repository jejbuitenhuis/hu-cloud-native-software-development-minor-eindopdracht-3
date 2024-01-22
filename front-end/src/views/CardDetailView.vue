<script setup lang="ts">
import {useRoute} from "vue-router";
import {ref} from "vue";
import DecoratedText from "@/components/DecoratedText.vue";
import type {PrintCard} from "@/models/cardModels";

const route = useRoute();
const loading = ref(true)
const card = ref<PrintCard | null>(null);

async function getCard() {
  const token = localStorage.getItem("jwtToken");
  if (!token) return;
  const response = await fetch(`/api/cards/${route.params["oracle_id"]}/${route.params["card_id"]}`, {headers: {Authorization: token}});
  if (!response.ok) {
    console.error(`Failed card fetch. Status: ${response.status}`)
    return;
  }
  const parsedData = await response.json() as any;
  card.value = parsedData['Items'][0] as PrintCard;
  loading.value = false;
}
getCard();
</script>

<template>
  <p v-if="loading" class="centered-content">Loading</p>
  <div v-if="!loading && card != null" class="card-wrapper">
    <div class="card-image">
      <img v-for="face in card.CardFaces" :src="face.ImageUrl" :alt="face.FaceName">
    </div>

    <div>
      <div class="card-info">
        <h2>{{ card.OracleName }}</h2>
        <DecoratedText :text="card.CardFaces[0].OracleText"/>
        <div v-for="face in card.CardFaces" class="face-info">
          <div>
            <p>{{ face.FaceName }}</p>
            <DecoratedText :text="face.ManaCost"/>
          </div>
          <p>{{ face.TypeLine }}</p>
          <DecoratedText :text="face.FlavorText"/>
        </div>
        <div>
          <sl-button class="add-to-collection-button">Add Card to Collection</sl-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
p {
  margin: 0;
}

.centered-content {
  margin-top: 20%;
  text-align: center;
}

.card-wrapper {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
  margin: 2rem;
}

.card-image img {
  max-width: 25rem;
}

.add-to-collection-button {
  margin-top: 1rem;
}

.face-info {
  border-top: 1px solid #333;
  margin-top: 0.5rem;
  padding-top: 0.5rem;

  >div {
    display: flex;
    gap: 1rem;
  }
}
</style>