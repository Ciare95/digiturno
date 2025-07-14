import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Importamos las rutas y la app
import Router from './router/index' 
import App from './App.vue'

//Importamos los estilos con tailwind
import './styles/style.css'

//Creamos la store y la app
const Pinia = createPinia()
const app = createApp(App)

app.use(Router).use(Pinia).mount('#app')