<template>
    <article class="cardItem">
        <RouterLink :to="{ path: '/cards/', query: { cardName: cardName } }">
            <span>{{ cardName }}</span>
            <div>
                <img class="image" :src="cardImageLink" :alt="cardName">
            </div>
        </RouterLink>
    </article>
</template>


<style scoped>
  .cardItem{
    max-width: 25%;
    padding: 0.4rem;
  }

  .image {
    height: auto;
    width: 100%;
    display: block;
    border-radius: 1rem;
  }
</style>


<script setup lang="ts">
    import { ref, onMounted } from 'vue';
    
    const cardObject = ref();
    const cardName = ref("");
    const cardOracle = ref("");
    const cardImageLink = ref("https://cards.scryfall.io/normal/front/d/9/d99a9a7d-d9ca-4c11-80ab-e39d5943a315.jpg?1632831210");

    const props = defineProps({
        cardObject : Object
    })

    onMounted(() => {
        cardObject.value = props.cardObject;
        cardName.value = cardObject.value.name
        cardOracle.value = cardObject.value.oracle_id;
        const imageUrls = cardObject.value.image_uris
        
        if(imageUrls){
            cardImageLink.value = imageUrls.normal;
        }
        

    });

</script>