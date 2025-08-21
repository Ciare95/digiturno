<template>
  <div class="empleado-charts">
    <!-- Estadísticas generales -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-800 mb-2">Total Empleados</h3>
        <p class="text-3xl font-bold text-blue-600">{{ estadisticasGenerales.total_empleados }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-800 mb-2">Turnos Hoy</h3>
        <p class="text-3xl font-bold text-green-600">{{ estadisticasGenerales.turnos_atendidos_hoy }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-800 mb-2">Calificación Promedio</h3>
        <p class="text-3xl font-bold text-yellow-600">{{ estadisticasGenerales.calificacion_promedio_general }}</p>
      </div>
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-800 mb-2">Mejor Empleado</h3>
        <p class="text-sm text-gray-600" v-if="estadisticasGenerales.empleado_mejor_calificacion">
          {{ estadisticasGenerales.empleado_mejor_calificacion.empleado__user__first_name }} 
          {{ estadisticasGenerales.empleado_mejor_calificacion.empleado__user__last_name }}
        </p>
        <p class="text-xs text-gray-500" v-else>Sin datos</p>
      </div>
    </div>

    <!-- Gráficos por empleado -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Gráfico de turnos atendidos -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Turnos Atendidos por Empleado</h3>
        <canvas ref="turnosChart" class="w-full h-64"></canvas>
      </div>

      <!-- Gráfico de calificaciones promedio -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Calificaciones Promedio</h3>
        <canvas ref="calificacionesChart" class="w-full h-64"></canvas>
      </div>

      <!-- Gráfico de tiempo promedio de atención -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Tiempo Promedio de Atención (min)</h3>
        <canvas ref="tiempoChart" class="w-full h-64"></canvas>
      </div>

      <!-- Gráfico de distribución de calificaciones -->
      <div class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Distribución de Calificaciones</h3>
        <canvas ref="distribucionChart" class="w-full h-64"></canvas>
      </div>
    </div>

    <!-- Tabla detallada de empleados -->
    <div class="mt-8 bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-800">Detalle por Empleado</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Empleado</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Turnos Hoy</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Turnos Semana</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Turnos Mes</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tiempo Prom. (min)</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Calificación</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Transferidos</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="empleado in empleados" :key="empleado.empleado_id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ empleado.empleado_nombre }}</div>
                <div class="text-sm text-gray-500">{{ empleado.empleado_email }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ empleado.turnos_atendidos_hoy }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ empleado.turnos_atendidos_semana }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ empleado.turnos_atendidos_mes }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ empleado.tiempo_promedio_atencion_minutos }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ empleado.calificacion_promedio }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ empleado.turnos_transferidos }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  name: 'EmpleadoCharts',
  props: {
    empleados: {
      type: Array,
      default: () => []
    },
    estadisticasGenerales: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
    const turnosChart = ref(null);
    const calificacionesChart = ref(null);
    const tiempoChart = ref(null);
    const distribucionChart = ref(null);

    let turnosChartInstance = null;
    let calificacionesChartInstance = null;
    let tiempoChartInstance = null;
    let distribucionChartInstance = null;

    const createCharts = () => {
      // Destruir charts existentes
      if (turnosChartInstance) turnosChartInstance.destroy();
      if (calificacionesChartInstance) calificacionesChartInstance.destroy();
      if (tiempoChartInstance) tiempoChartInstance.destroy();
      if (distribucionChartInstance) distribucionChartInstance.destroy();

      // Preparar datos
      const nombresEmpleados = props.empleados.map(e => e.empleado_nombre);
      const turnosHoy = props.empleados.map(e => e.turnos_atendidos_hoy);
      const calificaciones = props.empleados.map(e => e.calificacion_promedio);
      const tiempos = props.empleados.map(e => e.tiempo_promedio_atencion_minutos);

      // Calcular distribución total de calificaciones
      const distribucionTotal = { '1': 0, '2': 0, '3': 0, '4': 0, '5': 0 };
      props.empleados.forEach(empleado => {
        Object.entries(empleado.distribucion_calificaciones).forEach(([key, value]) => {
          distribucionTotal[key] += value;
        });
      });

      // Gráfico de turnos atendidos
      if (turnosChart.value) {
        turnosChartInstance = new Chart(turnosChart.value, {
          type: 'bar',
          data: {
            labels: nombresEmpleados,
            datasets: [{
              label: 'Turnos Atendidos Hoy',
              data: turnosHoy,
              backgroundColor: 'rgba(54, 162, 235, 0.6)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Cantidad de Turnos'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Empleados'
                }
              }
            }
          }
        });
      }

      // Gráfico de calificaciones promedio
      if (calificacionesChart.value) {
        calificacionesChartInstance = new Chart(calificacionesChart.value, {
          type: 'line',
          data: {
            labels: nombresEmpleados,
            datasets: [{
              label: 'Calificación Promedio',
              data: calificaciones,
              fill: false,
              borderColor: 'rgba(255, 206, 86, 1)',
              tension: 0.1,
              pointBackgroundColor: 'rgba(255, 206, 86, 1)',
              pointBorderColor: '#fff',
              pointHoverBackgroundColor: '#fff',
              pointHoverBorderColor: 'rgba(255, 206, 86, 1)'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                min: 0,
                max: 5,
                title: {
                  display: true,
                  text: 'Calificación (1-5)'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Empleados'
                }
              }
            }
          }
        });
      }

      // Gráfico de tiempo promedio
      if (tiempoChart.value) {
        tiempoChartInstance = new Chart(tiempoChart.value, {
          type: 'bar',
          data: {
            labels: nombresEmpleados,
            datasets: [{
              label: 'Tiempo Promedio (min)',
              data: tiempos,
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Minutos'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Empleados'
                }
              }
            }
          }
        });
      }

      // Gráfico de distribución de calificaciones
      if (distribucionChart.value) {
        distribucionChartInstance = new Chart(distribucionChart.value, {
          type: 'pie',
          data: {
            labels: ['1 Estrella', '2 Estrellas', '3 Estrellas', '4 Estrellas', '5 Estrellas'],
            datasets: [{
              data: Object.values(distribucionTotal),
              backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(255, 159, 64, 0.6)',
                'rgba(255, 205, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(54, 162, 235, 0.6)'
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 205, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(54, 162, 235, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        });
      }
    };

    onMounted(() => {
      if (props.empleados.length > 0) {
        createCharts();
      }
    });

    watch(() => props.empleados, (newEmpleados) => {
      if (newEmpleados.length > 0) {
        createCharts();
      }
    });

    return {
      turnosChart,
      calificacionesChart,
      tiempoChart,
      distribucionChart
    };
  }
};
</script>

<style scoped>
.empleado-charts {
  padding: 1rem;
}
</style>
