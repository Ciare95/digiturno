import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Importamos las rutas y la app
import router from './router/index' 
import App from './App.vue'

//Importamos los estilos con tailwind
import './styles/style.css'

//Creamos la store y la app
const Pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(Pinia)
app.mount('#app')