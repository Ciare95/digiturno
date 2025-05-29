import { createRouter, createWebHistory } from 'vue-router';


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

// Modo de desarrollo para permitir acceso sin backend
const MODO_DESARROLLO = true; // Cambiar a false cuando el backend esté listo

// Función para simular usuario en modo desarrollo
const simularUsuarioParaRuta = (ruta) => {
  // Extraer el rol de la ruta
  let rolSimulado = 'usuario';
  
  if (ruta.startsWith('/admin')) {
    rolSimulado = 'administrador';
  } else if (ruta.startsWith('/empleado')) {
    rolSimulado = 'empleado';
  } else if (ruta.startsWith('/usuario')) {
    rolSimulado = 'usuario';
  }
  
  // Crear usuario simulado según el rol
  return {
    id: 1,
    first_name: 'Usuario',
    last_name: 'Simulado',
    email: `${rolSimulado}@ejemplo.com`,
    rol: rolSimulado
  };
};

// Guardia de navegación para verificar autenticación
enrutador.beforeEach((to, from, next) => {
  if (MODO_DESARROLLO) {
    // En modo desarrollo, simular autenticación según la ruta
    if (to.matched.some(record => record.meta.requiereAutenticacion)) {
      const usuarioSimulado = simularUsuarioParaRuta(to.path);
      
      // Guardar en localStorage para que la aplicación funcione
      localStorage.setItem('usuario', JSON.stringify(usuarioSimulado));
      localStorage.setItem('token', 'token-simulado-desarrollo');
      
      // Permitir acceso
      next();
    } else {
      next();
    }
  } else {
    // Modo producción: verificación real de autenticación
    const token = localStorage.getItem('token');
    const usuario = JSON.parse(localStorage.getItem('usuario'));
    const estaAutenticado = !!token && !!usuario;
    
    // Verificar si la ruta requiere autenticación
    if (to.matched.some(record => record.meta.requiereAutenticacion)) {
      // Si no está autenticado, redirigir a inicio de sesión
      if (!estaAutenticado) {
        next({ name: 'iniciar-sesion' });
      } else {
        // Verificar rol si es necesario
        const rolRequerido = to.matched.find(record => record.meta.rol)?.meta.rol;
        if (rolRequerido && usuario.rol !== rolRequerido) {
          // Si el usuario no tiene el rol adecuado, redirigir según su rol
          if (usuario.rol === 'usuario') {
            next({ path: '/usuario' });
          } else if (usuario.rol === 'empleado') {
            next({ path: '/empleado' });
          } else if (usuario.rol === 'administrador') {
            next({ path: '/admin' });
          } else {
            next({ name: 'iniciar-sesion' });
          }
        } else {
          // Usuario autenticado y con rol correcto
          next();
        }
      }
    } else {
      // Ruta pública, permitir acceso
      next();
    }
  }
});

export default enrutador;
