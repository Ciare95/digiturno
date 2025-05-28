import { createApp } from 'vue'
import App from './App.vue'
import enrutador from './enrutador'
import { tienda } from './tienda'
import './assets/css/main.css'

// Importar FontAwesome para los iconos
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { 
  faUser, faUserTie, faBuilding, faHome, 
  faTicket, faTasks, faChartBar, faChartLine, faUsers, 
  faCog, faBell, faChevronDown, faSyncAlt, faMobileAlt
} from '@fortawesome/free-solid-svg-icons'

// Agregar iconos al conjunto
library.add(
  faUser, faUserTie, faBuilding, faHome, 
  faTicket, faTasks, faChartBar, faChartLine, faUsers, 
  faCog, faBell, faChevronDown, faSyncAlt, faMobileAlt
)

const app = createApp(App)

// Registrar componentes globales
app.component('font-awesome-icon', FontAwesomeIcon)

// Usar plugins
app.use(enrutador)
app.use(tienda)

// Montar la aplicación
app.mount('#app')
