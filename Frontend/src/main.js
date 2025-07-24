import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Importamos las rutas y la app
import Router from './router/index' 
import App from './App.vue'

// Importamos los estilos con tailwind
import './styles/style.css'

// Configuración de Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Importar los iconos que necesitamos
import { 
  faUserCog, 
  faCalendarPlus, 
  faMobileAlt, 
  faChartLine,
  faCog,
  faCalendarCheck,
  faCheckCircle
} from '@fortawesome/free-solid-svg-icons'

// Añadir los iconos a la librería
library.add(
  faUserCog, 
  faCalendarPlus, 
  faMobileAlt, 
  faChartLine,
  faCog,
  faCalendarCheck,
  faCheckCircle
)

// Creamos la store y la app
const Pinia = createPinia()
const app = createApp(App)

// Registrar el componente FontAwesomeIcon globalmente
app.component('font-awesome-icon', FontAwesomeIcon)

app.use(Router).use(Pinia).mount('#app')