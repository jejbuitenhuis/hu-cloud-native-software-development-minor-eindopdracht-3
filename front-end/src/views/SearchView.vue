<template>
    <div class="container">
        <h1>Search a card:</h1>
        <form @submit.prevent.submit="findCards" :class="{ 'disabled': formDisabled }">
            <sl-input v-model="searchQuery"></sl-input>
        </form>

        <section class="cardsContainer" >
            <Card :cardObject="card" class="card" v-for="card in cards"></Card>
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

.cardsContainer {
    display: flex;
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

const formDisabled = ref(false);
const formSubmitCount = ref(0);
const MAX_SUBMITS_PER_SECOND = 2;

function canSubmit(){
    if(formDisabled.value){
        return false;
    }

    formSubmitCount.value++;

    if(formSubmitCount.value >= MAX_SUBMITS_PER_SECOND){
        
        formDisabled.value = true;

        setTimeout(() => {
            formSubmitCount.value = 0;
            formDisabled.value = false;
        }, 3000);

        return false;
    } else{
        return true;
    }
}


async function findCards() {
    
    if(!canSubmit()){
        return;
    }

    let apiUrl : string = scryfallAPI!.value + "/cards/search?";
    const query = "q=" + searchQuery.value;
    apiUrl = apiUrl + query;
    
    const response = await requestCards(apiUrl);
    cards.value = response.data;
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