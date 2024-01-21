<script setup lang="ts">
import {useRoute} from "vue-router";
import {ref} from "vue";
import DecoratedText from "@/components/DecoratedText.vue";
import type {CombinedPrint, PrintCard, PrintFace, PrintPart} from "@/models/cardModels";

const route = useRoute();
const allPrints = ref<CombinedPrint[] | null>()
const oracle = ref<CombinedPrint | null>()
const loading = ref(true)

async function getOracle() {
  const token = localStorage.getItem("jwtToken");
  if (!token) return;
  const response = await fetch(`/api/cards?oracle_id=${route.params["oracle_id"]}`, {headers: {Authorization: token}});
  if (!response.ok) {
    console.error(`Failed oracle fetch. Status: ${response.status}`)
    return;
  }
  const data = await response.json() as PrintPart[];
  const combinedPrints: CombinedPrint[] = [];
  const cards = data.filter(v => v.DataType == "Card") as PrintCard[];
  const faces = data.filter(v => v.DataType == "Face") as PrintFace[];

  for (const card of cards) {
    combinedPrints.push({
      ...card,
      Faces: faces.filter(v => v.GSI1PK == card.GSI1PK)
    })
  }
  combinedPrints.sort((a, b) => new Date(b.ReleasedAt).getTime() - new Date(a.ReleasedAt).getTime())
  allPrints.value = combinedPrints;
  oracle.value = combinedPrints[0];
  loading.value = false;
}
getOracle();
</script>

<template>
  <p v-if="loading" class="centered-content">Loading</p>
  <div v-if="!loading && oracle != null" class="oracle-wrapper">
    <div class="oracle-image">
      <img v-for="face in oracle.Faces" :src="face.ImageUrl" :alt="face.FaceName">
    </div>

    <div>
      <div class="oracle-info">
        <h2>{{ oracle.OracleName }}</h2>
        <DecoratedText :text="oracle.Faces[0].OracleText"/>
        <div v-for="face in oracle.Faces" class="face-info">
          <div>
            <p>{{ face.FaceName }}</p>
            <DecoratedText :text="face.ManaCost"/>
          </div>
          <p>{{ face.TypeLine }}</p>
          <DecoratedText :text="face.FlavorText"/>
        </div>
      </div>

      <div class="prints-info">
        <table>
          <thead>
          <tr>
            <th>Set name</th>
            <th>Release date</th>
            <th>Rarity</th>
            <th>Price</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="print in allPrints">
            <td>{{ print.SetName }}</td>
            <td>{{ new Date(print.ReleasedAt).toLocaleDateString("nl-nl") }}</td>
            <td>{{ print.Rarity }}</td>
            <td>{{ print.Price == null ? "-" : `€${print.Price}` }}</td>
            <td><router-link :to="`/cards/${print.GSI1PK.replace('PrintId#', '')}`">View</router-link></td>
          </tr>
          </tbody>
        </table>
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

.oracle-wrapper {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 2rem;
  margin: 2rem;
}

.oracle-image img {
  max-width: 25rem;
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

.prints-info {
  background-color: #333;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-top: 1rem;
}

table {
  border-spacing: 1rem 0;

  th {
    text-align: left;
  }
}
</style>