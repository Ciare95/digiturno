import { createRouter, createWebHistory } from "vue-router";

//Importamos las vistas
import Home from '../views/Home.vue';
import SolicitarTurno from "../views/SolicitarTurno.vue";
import Login from "../views/Login.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import EmpleadoDashboard from "../views/EmpleadoDashboard.vue";

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
        meta: { requiresAuth: true },
    },
    {
        path: '/login',
        component: Login,
        meta: { guestOnly: true }
    },
    {
        path: '/admin',
        component: AdminDashboard,
        meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
        path: '/empleado',
        component: EmpleadoDashboard,
        meta: { requiresAuth: true, requiresEmpleado: true }
    }
]

//Creamos el router con las rutas
const Router = createRouter({
    history: createWebHistory(), 
    routes
});

// Guard de navegación
/*
Router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('token'); // Verifica si hay un token guardado
    const userRole = localStorage.getItem('userRole'); // Obtener el rol del usuario
    
    // Verificar si la ruta requiere autenticación
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!isAuthenticated) {
            next('/login');
        } else if (to.matched.some(record => record.meta.requiresAdmin) && userRole !== 'admin') {
            // Si la ruta requiere ser admin y el usuario no lo es, redirigir al home
            next('/');
        } else if (to.matched.some(record => record.meta.requiresEmpleado) && userRole !== 'empleado' && userRole !== 'admin') {
            // Si la ruta es para empleados y el usuario no tiene permiso
            next('/');
        } else {
            next();
        }
    } else if (to.matched.some(record => record.meta.guestOnly) && isAuthenticated) {
        // Si el usuario está autenticado y trata de acceder a una ruta de invitado
        next('/');
    } else {
        next();
    }
});
*/
//Exportamos el router
export default Router;