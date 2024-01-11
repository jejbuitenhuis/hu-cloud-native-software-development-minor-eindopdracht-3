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