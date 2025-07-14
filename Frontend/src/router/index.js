import { createRouter, createWebHistory } from "vue-router";

//Importamos las vistas
import Home from '../views/Home.vue';

//Creamos las rutas
const routes = [
    { 
        path: '/',
        component: Home
    }
]

//Creamos el router con las rutas
const Router = createRouter({
    history: createWebHistory(), 
    routes
});

//Exportamos el router
export default Router;