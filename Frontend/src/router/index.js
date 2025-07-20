import { createRouter, createWebHistory } from "vue-router";

//Importamos las vistas
import Home from '../views/Home.vue';
import SolicitarTurno from "../views/SolicitarTurno.vue";

//Creamos las rutas
const routes = [
    { 
        path: '/',
        component: Home
    },
    {
        path: '/solicitar-turno',
        component: SolicitarTurno
    }
]

//Creamos el router con las rutas
const Router = createRouter({
    history: createWebHistory(), 
    routes
});

//Exportamos el router
export default Router;