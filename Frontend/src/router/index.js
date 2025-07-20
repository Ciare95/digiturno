import { createRouter, createWebHistory } from "vue-router";

//Importamos las vistas
import Home from '../views/Home.vue';
import SolicitarTurno from "../views/SolicitarTurno.vue";
import Login from "../views/Login.vue";

//Creamos las rutas
const routes = [
    { 
        path: '/',
        component: Home,
        meta: { requiresAuth: true }
    },
    {
        path: '/solicitar-turno',
        component: SolicitarTurno,
        meta: { requiresAuth: true }
    },
    {
        path: '/login',
        component: Login,
        meta: { guestOnly: true }
    }
]

//Creamos el router con las rutas
const Router = createRouter({
    history: createWebHistory(), 
    routes
});

// Guard de navegación
Router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('token'); // Verifica si hay un token guardado
    
    if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
        next('/login');
    } else if (to.matched.some(record => record.meta.guestOnly) && isAuthenticated) {
        next('/');
    } else {
        next();
    }
});

//Exportamos el router
export default Router;