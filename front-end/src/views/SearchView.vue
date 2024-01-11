<template>
    <div class="container">
        <h1>Search a card:</h1>
        <form @submit.prevent.submit="findCards">
            <sl-input v-model="searchQuery"></sl-input>
        </form>

        <section class="cards" >
            <Card class="card" v-for="card in cards"></Card>
        </section>

    </div>
</template>

<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 1rem;
    flex-direction: column;
}

.cards {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    padding-top: 1rem;
    width: 80%;
}
</style>


<script setup lang="ts">

import { ref, inject} from 'vue';
import type { Ref } from "vue";

import Card from '../components/Card.vue';

const scryfallAPI = inject<Ref<string>>('ScryfallAPI');
const searchQuery = ref('');
const cards = ref([]);

async function findCards() {
    let apiUrl : string = scryfallAPI!.value + "/cards/search?";
    const query = "q=" + searchQuery.value;
    apiUrl = apiUrl + query;
    
    const response = await requestCards(apiUrl);
}

async function requestCards(scryfallAPI: string) : Promise<any>{
    try {
        const response = await fetch(scryfallAPI,
            {
                "method": "get",
                "headers": {
                    "Content-Type": "application/json"
                },
            }
        );

        if(!response.ok){
            throw new Error("HTTP error couldn't fetch the data")
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}


</script>