<template>
<sl-card class="card-header">
<h1>Register</h1>
<form id="login-form" @submit.prevent.submit="register">
    <sl-input label="Email" id="email" type="email" placeholder="Email" required v-model="email" ref="emailInput"></sl-input>
    <sl-input label="Password" id="password" password-toggle placeholder="Password" type="password" required v-model="password" @sl-input="handleInput" ref="passwordInput"></sl-input>
    <sl-input label="Re-enter password" id="confirm" password-toggle placeholder="Confirm password" type="password" required v-model="confirmPassword" @sl-input="handleInput" ref="passwordConfirmInput"></sl-input>
    <p id="error-message" v-if="errorMessage">{{ errorMessage }}</p>
    <sl-button class="confirm" variant="primary" type="submit">Confirm</sl-button>
    <sl-button class="gologin" variant="neutral" @click="router.push('/login')">To login</sl-button>
</form>
</sl-card>
</template>


<!-- SCRIPT -->


<script setup lang="ts">
import "@shoelace-style/shoelace/dist/components/input/input";
import '@shoelace-style/shoelace/dist/components/card/card';
import type SlInput from "@shoelace-style/shoelace/dist/components/input/input";
import { ref, type Ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const email = ref('');
const password = ref('');
const confirmPassword = ref('');

const emailInput : Ref<null> | Ref<HTMLObjectElement> = ref(null);
const passwordInput : Ref<null> | Ref<HTMLObjectElement> = ref(null);
const passwordConfirmInput : Ref<null> | Ref<HTMLObjectElement> = ref(null);

const errorMessage = ref('');

const router = useRouter();

function register(){
    if (!isFormValid()) {
        return
    }
    console.log("submitted");
    sendData(email.value, password.value)
        .then((response) => {
            if (response.status === 409){
                showErrorMessage("This email adress has already been registered!");
            }
            if (response.ok) {
                alert("We have send you an email to verify your email adress.");
                router.push("/login");
            } else {
                showErrorMessage(`Something went wrong: \n${response.statusText}`);
            }
        });
}

function showErrorMessage(error : string){
    console.log(error);
    errorMessage.value = error;
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

function isFormValid() : boolean{
    // @ts-ignore typescript detecteerd het bestaan van getAttribute() niet
    if (emailInput.value.getAttribute('data-invalid') === ''){
        return false;
    }
    // @ts-ignore typescript detecteerd het bestaan van getAttribute() niet
    if (passwordInput.value.getAttribute('data-invalid') === ''){
        return false;
    }
    // @ts-ignore typescript detecteerd het bestaan van getAttribute() niet
    if (passwordConfirmInput.value.getAttribute('data-invalid') === ''){
        return false;
    }

    return true;
}

async function sendData(email : string, password : string){
    return await fetch("/api/auth/register", {
        "method" : "post",
        "mode" : "cors",
        "headers" : {
            "Content-Type" : "application/json"
        },
        "body" : JSON.stringify({
            "email" : email,
            "password" : password
        })
    }
    )
}
</script>


<!-- STYLE -->


<style scoped lang="scss">
.confirm {
    width: 100%;
}
.gologin {
    width: 100%;
    margin-top: 5px;
}
</style>