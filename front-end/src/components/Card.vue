<template>
    <sl-card class="cardItem">
        <a>
            <span>{{ cardName }}</span>
            <div>
                <img :src="cardImageLink" :alt="cardName">
            </div>
        </a>
    </sl-card>
</template>


<style scoped>
  .cardItem{
    height: fit-content;
    width: fit-content;
  }
</style>


<script setup lang="ts">
    import "@shoelace-style/shoelace/dist/components/input/input";
    import '@shoelace-style/shoelace/dist/components/card/card';
    import '@shoelace-style/shoelace/dist/components/button/button';
    
    import { ref } from 'vue';

    const cardName = ref("");
    const cardImageLink = ref("");

</script>