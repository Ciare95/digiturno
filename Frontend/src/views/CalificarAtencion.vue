<template>
    <div class="max-w-3xl mx-auto p-6">
    <header class="mb-6">
      <h1 class="text-2xl font-bold">Calificar atención</h1>
      <p class="text-sm text-gray-600">
        Cuéntanos cómo te fue. Tus comentarios nos ayudan a mejorar.
      </p>
    </header>

    <!-- Cargando / Error -->
    <div v-if="loading" class="py-10 text-center">Cargando turno…</div>
    <div v-else-if="error" class="p-4 bg-red-100 text-red-700 rounded">{{ error }}</div>

    <!-- Éxito -->
    <div v-else-if="exito" class="p-6 bg-green-50 border border-green-200 rounded">
      <h2 class="text-lg font-semibold text-green-800">¡Gracias por tu calificación! 🎉</h2>
      <p class="text-sm text-green-700 mt-2">
        Tu opinión quedó registrada.
      </p>
      <div class="mt-4 flex gap-3">
        <button @click="irHistorial" class="px-4 py-2 border rounded hover:bg-green-100">
          Ver mi historial
        </button>
        <button @click="irInicio" class="px-4 py-2 border rounded hover:bg-green-100">
          Ir al inicio
        </button>
      </div>
    </div>

    <!-- Formulario -->
    <div v-else class="space-y-6">
      <section class="p-4 border rounded bg-white">
        <div class="text-sm text-gray-500">Turno</div>
        <div class="font-semibold text-lg">
          {{ turno?.numero_turno || '—' }}
        </div>
        <div class="text-sm text-gray-600">
          {{ turno?.servicio_nombre || '—' }} • {{ turno?.sucursal_nombre || '—' }}
        </div>
        <div class="text-xs text-gray-500 mt-1">
          Finalizado: {{ ffecha(turno?.fecha_finalizacion) }}
        </div>
        <div v-if="!turnoValido" class="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded text-sm text-yellow-800">
          Solo puedes calificar turnos finalizados, cancelados o ausentes.
        </div>
      </section>

      <!-- Estrellas -->
      <section class="p-4 border rounded bg-white">
        <label class="block font-medium mb-2">Calificación (1–5)</label>
        <div class="flex items-center gap-2">
          <button
            v-for="i in 5"
            :key="i"
            type="button"
            :aria-label="`calificar ${i}`"
            @click="form.rating = i"
            class="p-1"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
                 class="w-8 h-8"
                 :class="i <= form.rating ? 'fill-yellow-400 stroke-yellow-500' : 'fill-transparent stroke-gray-300'">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.967 0 1.371 1.24.588 1.81l-2.802 2.035a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.538 1.118l-2.802-2.035a1 1 0 00-1.175 0l-2.802 2.035c-.783.57-1.838-.197-1.538-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.88 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
          </button>
        </div>
        <p v-if="errores.rating" class="text-sm text-red-600 mt-2">{{ errores.rating }}</p>
      </section>

      <!-- NPS -->
      <section class="p-4 border rounded bg-white">
        <div class="flex items-center justify-between">
          <label class="block font-medium">¿Qué tan probable es que nos recomiendes? (0–10)</label>
          <span class="text-sm font-semibold">{{ form.nps }}</span>
        </div>
        <input type="range" min="0" max="10" v-model.number="form.nps" class="w-full mt-2" />
        <div class="flex justify-between text-xs text-gray-500">
          <span>0 Nada probable</span>
          <span>10 Muy probable</span>
        </div>
      </section>

      <!-- Etiquetas -->
      <section class="p-4 border rounded bg-white">
        <label class="block font-medium mb-2">¿Qué destacas?</label>
        <div class="flex flex-wrap gap-2">
          <label v-for="t in etiquetasDisponibles" :key="t" class="inline-flex items-center gap-2 px-3 py-2 border rounded-full text-sm cursor-pointer">
            <input type="checkbox" :value="t" v-model="form.etiquetas" />
            <span>{{ t }}</span>
          </label>
        </div>
      </section>

      <!-- Comentario -->
      <section class="p-4 border rounded bg-white">
        <label class="block font-medium mb-2">Comentario (opcional)</label>
        <textarea
          v-model.trim="form.comentario"
          :maxlength="MAX_COMENTARIO"
          rows="4"
          class="w-full border rounded p-3"
          placeholder="¿Qué salió muy bien? ¿Qué podemos mejorar?"
        ></textarea>
        <div class="text-xs text-gray-500 mt-1">
          {{ form.comentario.length }}/{{ MAX_COMENTARIO }} caracteres
        </div>
      </section>

      <!-- Anónimo -->
      <section class="p-4 border rounded bg-white">
        <label class="inline-flex items-center gap-2">
          <input type="checkbox" v-model="form.anonimo" />
          <span class="text-sm">Enviar de forma anónima</span>
        </label>
      </section>

      <!-- Acciones -->
      <div class="flex items-center gap-3">
        <button
          :disabled="enviando || !turnoValido"
          @click="enviar"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {{ enviando ? 'Enviando…' : 'Enviar calificación' }}
        </button>
        <button @click="irHistorial" class="px-4 py-2 border rounded hover:bg-gray-50">
          Cancelar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import dayjs from 'dayjs'
import 'dayjs/locale/es'
import api from '@/Services/api'
dayjs.locale('es')

const route = useRoute()
const router = useRouter()
const turnoId = route.params.id

const loading = ref(true)
const enviando = ref(false)
const exito = ref(false)
const error = ref('')
const turno = ref(null)

const MAX_COMENTARIO = 500
const etiquetasDisponibles = [
  'Amabilidad',
  'Claridad',
  'Tiempo de espera',
  'Solución efectiva',
  'Empatía',
  'Conocimiento',
  'Tiempo de atención',
  'Instalaciones',
]

const form = ref({
  rating: 0,          // 1..5
  nps: 10,            // 0..10
  etiquetas: [],
  comentario: '',
  anonimo: false,
})

const errores = ref({})

const turnoValido = computed(() => {
  const e = (turno.value?.estado || '').toLowerCase()
  return ['finalizado', 'cancelado', 'ausente'].includes(e)
})

function ffecha(v) {
  return v ? dayjs(v).format('DD MMM YYYY • HH:mm') : '—'
}

async function cargarTurno() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get(`/turnos/${turnoId}/`)
    turno.value = data
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || 'No fue posible cargar el turno'
  } finally {
    loading.value = false
  }
}

function validar() {
  const errs = {}
  if (!form.value.rating || form.value.rating < 1 || form.value.rating > 5) {
    errs.rating = 'Selecciona entre 1 y 5 estrellas'
  }
  errores.value = errs
  return Object.keys(errs).length === 0
}

async function enviar() {
  if (!validar()) return
  enviando.value = true
  error.value = ''
  try {
    await api.post(`/turnos/${turnoId}/calificar/`, {
      rating: form.value.rating,
      nps: form.value.nps,
      etiquetas: form.value.etiquetas,
      comentario: form.value.comentario,
      anonimo: form.value.anonimo,
      fuente: 'web',
    })
    exito.value = true
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || 'No fue posible registrar la calificación'
  } finally {
    enviando.value = false
  }
}

function irHistorial() {
  router.push({ name: 'Historial' })
}
function irInicio() {
  router.push({ path: '/' })
}

onMounted(cargarTurno)
</script>