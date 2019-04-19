<template>
    <div>
        <input v-model="login" type="text" placeholder="Login"/>
        <input v-model="password" type="password" placeholder="Password"/>
        <button @click="SignIn"> Sign In </button>
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
                        console.log(response)
                    },
                    error: (response) => {
                        console.log(response)
                    }
                })
            }
        }
    }
</script>

<style scoped>

</style>
