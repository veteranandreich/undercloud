import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Feed from '@/components/Feed'
import Register from '@/components/Register'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/login',
            name: 'Login',
            component: Login
        },

        {
            path: '/feed',
            name: 'Feed',
            component: Feed
        },
        {
            path: '/register',
            name: 'Register',
            component: Register
        }

    ]
})
