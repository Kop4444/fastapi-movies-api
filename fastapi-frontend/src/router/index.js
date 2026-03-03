import { createRouter, createWebHistory } from 'vue-router'
import MovieList from '../components/pages/MovieList.vue'
import MovieCreate from '../components/pages/MovieCreate.vue'
import MovieEdit from '../components/pages/MovieEdit.vue'
import MovieShow from '../components/pages/MovieShow.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: MovieList },
    { path: '/create', component: MovieCreate },
    { path: '/edit/:id', component: MovieEdit },
    { path: '/show/:id', component: MovieShow },
  ]
})

export default router