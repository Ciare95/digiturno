import { createRouter, createWebHistory } from 'vue-router';
import { tienda } from '../tienda';

// Importación de layouts
const LayoutPrincipal = () => import('../layouts/LayoutPrincipal.vue');
const LayoutAutenticado = () => import('../layouts/LayoutAutenticado.vue');

// Importación de vistas públicas
const Inicio = () => import('../vistas/Inicio.vue');
const IniciarSesion = () => import('../vistas/IniciarSesion.vue');
const Registro = () => import('../vistas/Registro.vue');
const NoEncontrado = () => import('../vistas/NoEncontrado.vue');

// Importación de vistas de usuario
const PanelUsuario = () => import('../vistas/usuario/Panel.vue');
const TurnosUsuario = () => import('../vistas/usuario/Turnos.vue');
const PerfilUsuario = () => import('../vistas/usuario/Perfil.vue');

// Importación de vistas de empleado
const PanelEmpleado = () => import('../vistas/empleado/Panel.vue');
const GestionTurnos = () => import('../vistas/empleado/GestionTurnos.vue');
const EstadisticasEmpleado = () => import('../vistas/empleado/Estadisticas.vue');

// Importación de vistas de administrador
const PanelAdmin = () => import('../vistas/administrador/Panel.vue');
const GestionUsuarios = () => import('../vistas/administrador/GestionUsuarios.vue');
const GestionEmpleados = () => import('../vistas/administrador/GestionEmpleados.vue');
const GestionSucursales = () => import('../vistas/administrador/GestionSucursales.vue');
const GestionServicios = () => import('../vistas/administrador/GestionServicios.vue');
const EstadisticasAdmin = () => import('../vistas/administrador/Estadisticas.vue');
const Configuracion = () => import('../vistas/administrador/Configuracion.vue');

// Definición de rutas
const rutas = [
  {
    path: '/',
    component: LayoutPrincipal,
    children: [
      {
        path: '',
        name: 'inicio',
        component: Inicio
      },
      {
        path: 'iniciar-sesion',
        name: 'iniciar-sesion',
        component: IniciarSesion
      },
      {
        path: 'registro',
        name: 'registro',
        component: Registro
      }
    ]
  },
  {
    path: '/usuario',
    component: LayoutAutenticado,
    meta: { requiereAutenticacion: true, rol: 'usuario' },
    children: [
      {
        path: '',
        name: 'panel-usuario',
        component: PanelUsuario
      },
      {
        path: 'turnos',
        name: 'turnos-usuario',
        component: TurnosUsuario
      },
      {
        path: 'perfil',
        name: 'perfil-usuario',
        component: PerfilUsuario
      }
    ]
  },
  {
    path: '/empleado',
    component: LayoutAutenticado,
    meta: { requiereAutenticacion: true, rol: 'empleado' },
    children: [
      {
        path: '',
        name: 'panel-empleado',
        component: PanelEmpleado
      },
      {
        path: 'gestion-turnos',
        name: 'gestion-turnos',
        component: GestionTurnos
      },
      {
        path: 'estadisticas',
        name: 'estadisticas-empleado',
        component: EstadisticasEmpleado
      }
    ]
  },
  {
    path: '/admin',
    component: LayoutAutenticado,
    meta: { requiereAutenticacion: true, rol: 'administrador' },
    children: [
      {
        path: '',
        name: 'panel-admin',
        component: PanelAdmin
      },
      {
        path: 'usuarios',
        name: 'gestion-usuarios',
        component: GestionUsuarios
      },
      {
        path: 'empleados',
        name: 'gestion-empleados',
        component: GestionEmpleados
      },
      {
        path: 'sucursales',
        name: 'gestion-sucursales',
        component: GestionSucursales
      },
      {
        path: 'servicios',
        name: 'gestion-servicios',
        component: GestionServicios
      },
      {
        path: 'estadisticas',
        name: 'estadisticas-admin',
        component: EstadisticasAdmin
      },
      {
        path: 'configuracion',
        name: 'configuracion',
        component: Configuracion
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'no-encontrado',
    component: NoEncontrado
  }
];

// Creación del enrutador
const enrutador = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: rutas
});

// Guardia de navegación para proteger rutas según roles
enrutador.beforeEach((to, from, next) => {
  const requiereAutenticacion = to.matched.some(record => record.meta.requiereAutenticacion);
  const usuario = tienda.state.usuario;
  const estaAutenticado = !!usuario;
  
  if (requiereAutenticacion && !estaAutenticado) {
    next({ name: 'iniciar-sesion', query: { redirect: to.fullPath } });
  } else if (requiereAutenticacion && estaAutenticado) {
    const rolRequerido = to.matched.find(record => record.meta.rol)?.meta.rol;
    
    if (rolRequerido && usuario.rol !== rolRequerido) {
      // Redirigir al panel correspondiente según el rol del usuario
      if (usuario.rol === 'usuario') {
        next({ name: 'panel-usuario' });
      } else if (usuario.rol === 'empleado') {
        next({ name: 'panel-empleado' });
      } else if (usuario.rol === 'administrador') {
        next({ name: 'panel-admin' });
      } else {
        next({ name: 'inicio' });
      }
    } else {
      next();
    }
  } else {
    next();
  }
});

export default enrutador;
