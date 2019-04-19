<template>
    <div>
        Твой Feed
        <ul>
            <li v-for="profile in profiles">
                {{profile.owner.username}}

            </li>
        </ul>

    </div>
</template>

<script>
    import $ from 'jquery'
    export default {
        name: "Feed",
        data() {
            return {
                profiles: ''
            }
        },
        created() {
            this.AjaxSetup();
            $.ajax({
                url: ("http://127.0.0.1:8000/api/profiles"),
                type: "GET",
                success: (response) => {
                    console.log(response);
                    this.profiles = response
                },
                error: (response) => {
                    console.log(response)
                }
            })
        },
        methods: {
            // Сделать из этой функции глобальный миксин
            AjaxSetup() {
                if (localStorage.getItem("refresh_token")) {
                $.ajax({
                url: "http://127.0.0.1:8000/api/jwt-refresh/",
                type: "POST",
                dataType: 'json',
                crossDomain: true,
                header: {},
                data: {
                    refresh: localStorage.getItem("refresh_token")
                },
                success: (response) => {
                    localStorage.setItem("access_token", response.access)
                },
                error: (response) => {
                    console.log(response);
                }
                });
                $.ajaxSetup({
                    headers: {
                        'Authorization': "Bearer " + localStorage.getItem("access_token")
                }
                });

                }

                else{
                    this.$router.push("Login")
                }
            }
        }
    }
</script>

<style scoped>

</style>
