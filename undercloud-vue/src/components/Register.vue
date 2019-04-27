<template>
    <div>
        <p><input v-model="login" type="text" placeholder="Login"/></p>
        <p v-if="usernamemessage"> <p v-for="er1 in usernamemessage"> {{er1}} </p> </p>
        <p><input v-model="email" type="email" placeholder="Email"></p>
        <p v-if="emailmessage"> <p v-for="er2 in emailmessage"> {{er2}} </p> </p>
        <p><input v-model="password1" type="password" placeholder="Password"/></p>
        <p><input v-model="password2" type="password" placeholder="Confirm your password"/></p>
        <button @click="SignUp"> Sign Up </button>
        <div v-if="password1 !== password2"> Passwords don't match</div>
        <router-link :to="{name: 'Login'}">
            Already have an account?
        </router-link>
    </div>
</template>

<script>
    import $ from 'jquery'

    export default {
        name: "Register",
        data() {
            return {
                login: '',
                email: '',
                password1: '',
                password2: '',
                usernamemessage: '',
                emailmessage: '',
            }
        },
        methods: {
            SignUp(){
                if (this.password1 === this.password2) {
                    $.ajax({
                        url: "http://127.0.0.1:8000/api/register",
                        type: "POST",
                        dataType: 'json',
                        crossDomain: true,
                        header: {},
                        data: {
                            username: this.login,
                            email: this.email,
                            password: this.password1
                        },
                        success: (response) => {
                            alert("We've sent you confirmation email, please verify your account and start using our service");
                            this.$router.push("Login")

                        },
                        error: (response) => {
                            console.log(response);
                            this.usernamemessage = response.responseJSON.username;
                            this.emailmessage = response.responseJSON.email
                        }
                    })
                }
            }
        }
    }

</script>

<style scoped>

</style>
