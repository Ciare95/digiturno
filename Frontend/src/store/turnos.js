import { defineStore } from 'pinia';
import { solicitarTurno as solicitarTurnoAPI } from '@/services/SolicitarTurno';

export const useTurnosStore = defineStore('turnos', {
  state: () => ({
    turnos: [],
    contadorTurnos: {
      caja: 0,
      asesoria: 0,
      pagos: 0,
      informacion: 0
    }
  }),

  getters: {
    turnosEnEspera: (state) => {
      return [...state.turnos].filter(turno => !turno.atendido);
    },
    turnosAtendidos: (state) => {
      return [...state.turnos].filter(turno => turno.atendido);
    },
    // Obtener el número de turnos por servicio
    conteoPorServicio: (state) => {
      return state.turnos.reduce((acc, turno) => {
        acc[turno.servicio] = (acc[turno.servicio] || 0) + 1;
        return acc;
      }, {});
    }
  },

  actions: {
    generarCodigo(servicio) {
      const prefijos = {
        caja: 'C',
        asesoria: 'A',
        pagos: 'P',
        informacion: 'I'
      };
      
      this.contadorTurnos[servicio] = (this.contadorTurnos[servicio] || 0) + 1;
      return `${prefijos[servicio]}${this.contadorTurnos[servicio].toString().padStart(3, '0')}`;
    },

    async solicitarTurno(datosTurno) {
      const nuevoTurno = {
        id: Date.now(),
        codigo: this.generarCodigo(datosTurno.servicio),
        servicio: datosTurno.servicio,
        nombre: datosTurno.nombre,
        documento: datosTurno.documento,
        sucursalId: datosTurno.sucursalId,
        sucursal: datosTurno.sucursal,
        horaSolicitud: new Date().toISOString(),
        atendido: false
      };

      this.turnos.unshift(nuevoTurno);
      return nuevoTurno;
    },

    async agregarTurno(datosTurno) {
      // Prepara el payload para el backend
      const payload = {
        servicio: datosTurno.servicio,
        sucursal: datosTurno.sucursalId,
        numero_cedula: datosTurno.documento,
        nombre_cliente: datosTurno.nombre
      };
      // Llama al backend
      const turnoGenerado = await solicitarTurnoAPI(payload);
      // Puedes guardar el turno en el estado si lo deseas
      this.turnos.unshift(turnoGenerado);
      return turnoGenerado;
    },

    marcarAtendido(id) {
      const turno = this.turnos.find(t => t.id === id);
      if (turno) {
        turno.atendido = true;
        turno.horaAtencion = new Date().toISOString();
      }
    }
  }
});
