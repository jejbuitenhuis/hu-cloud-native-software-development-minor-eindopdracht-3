<template>
<h1>Register</h1>
<form id="login-form" @submit.prevent="register">
    <sl-input label="Email" id="email" type="email" placeholder="Email" required v-model="username" ref="usernameInput"></sl-input>
    <sl-input label="Password" id="password" password-toggle placeholder="Password" type="password" required v-model="password" @sl-input="handleInput" ref="passwordInput"></sl-input>
    <sl-input label="Re-enter password" id="confirm" password-toggle placeholder="Confirm password" type="password" required v-model="confirmPassword" @sl-input="handleInput" ref="passwordConfirmInput"></sl-input>
    <br><p id="error-message" v-if="errorMessage">{{ errorMessage }}</p>
    <sl-button class="confirm" type="submit">Confirm</sl-button>
</form>

</template>

<script setup lang="ts">
import "@shoelace-style/shoelace/dist/components/input/input";
import type SlInput from "@shoelace-style/shoelace/dist/components/input/input";
import { onMounted, ref, type Ref } from "vue";

const username = ref('');
const password = ref('');
const confirmPassword = ref('');

const usernameInput : Ref<null> | Ref<HTMLObjectElement> = ref(null);
const passwordInput : Ref<null> | Ref<HTMLObjectElement> = ref(null);
const passwordConfirmInput : Ref<null> | Ref<HTMLObjectElement> = ref(null);

const errorMessage = ref('');


function register(){
    console.log("submitted");
}

function handleInput(){
    if (passwordConfirmInput.value === null) {
        throw "Where did the password confirm field go?"
    }

    // @ts-ignore typescript zeikt over dat hij niet weet dat het html element een value heeft
    confirmPassword.value = passwordConfirmInput.value.value;
    // @ts-ignore typescript zeikt over dat hij niet weet dat het html element een value heeft
    password.value = passwordInput.value.value;

    if (password.value === confirmPassword.value) {
        passwordConfirmInput.value.setCustomValidity('');
    } else {
        passwordConfirmInput.value.setCustomValidity('Passwords must match!');
    }
}


</script>


<style scoped lang="scss">
.confirm {
    width: 100%;
}
</style>