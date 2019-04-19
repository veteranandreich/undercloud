<template>
    <div>
        <input v-model="login" type="text" placeholder="Login"/>
        <input v-model="password" type="password" placeholder="Password"/>
        <button @click="SignIn"> Sign In </button>
        <router-link :to="{name: 'Register'}">
            New here?
        </router-link>
        <hr>
        {{errormessage}}
    </div>
</template>

<script>
    import $ from 'jquery'


    export default {
        name: "Login",
        data() {
            return {
                login: '',
                password: '',
                errormessage: ''
            }
        },
        methods: {
            SignIn() {
                $.ajax({
                    url: "http://127.0.0.1:8000/api/jwt-auth/",
                    type: "POST",
                    dataType: 'json',
                    crossDomain: true,
                    header: {

                    },
                    data: {
                        username: this.login,
                        password: this.password
                    },
                    success: (response) => {
                        this.errormessage = "";
                        console.log(response);
                        localStorage.setItem("access_token", response.access)
                        localStorage.setItem("refresh_token", response.refresh)
                        this.$router.push("Feed")

                    },
                    error: (response) => {
                        console.log(response);
                        this.errormessage = "Incorrect login or password"
                    }
                })
            }
        }
    }
</script>

<style scoped>

</style>
