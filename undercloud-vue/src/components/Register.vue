<template>
    <div>
        <p><input v-model="login" type="text" placeholder="Login"/></p>
        <p><input v-model="email" type="email" placeholder="Email"></p>
        <p><input v-model="password1" type="password" placeholder="Password"/></p>
        <p><input v-model="password2" type="password" placeholder="Confirm your password"/></p>
        <button @click="SignUp"> Sign Up </button>
        <div v-if="password1 !== password2"> Passwords don't match</div>
        <router-link :to="{name: 'Login'}">
            Already have an account?
        </router-link>
        <hr>
        {{errormessage}}
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
                errormessage: ''
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
                            this.errormessage = "Incorrect data, make sure all fields are filled"
                        }
                    })
                }
            }
        }
    }

</script>

<style scoped>

</style>
