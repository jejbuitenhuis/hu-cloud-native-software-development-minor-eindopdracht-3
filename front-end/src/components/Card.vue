<template>
    <article class="cardItem">
        <a>
            <span>{{ cardName }}</span>
            <div>
                <img class="image" src="../assets/testcard.jpg" :alt="cardName">
            </div>
        </a>
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
    import "@shoelace-style/shoelace/dist/components/input/input";
    import '@shoelace-style/shoelace/dist/components/card/card';
    import '@shoelace-style/shoelace/dist/components/button/button';
    import { ref, onMounted } from 'vue';
    
    const cardObject = ref();
    const cardName = ref("");
    const cardImageLink = ref("");

    const props = defineProps({
        cardObject : Object
    })

    onMounted(() => {
        cardObject.value = props.cardObject;
        console.log(cardObject.value)
    });

</script>