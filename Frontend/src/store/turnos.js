import { defineStore } from 'pinia';

export const useTurnosStore = defineStore('turnos', {
  state: () => ({
    turnos: [],
    contadorTurnos: {
      caja: 0,
      asesoria: 0,
      pagos: 0
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
        pagos: 'P'
      };
      
      this.contadorTurnos[servicio] += 1;
      return `${prefijos[servicio]}${this.contadorTurnos[servicio].toString().padStart(3, '0')}`;
    },

    async solicitarTurno(datosTurno) {
      const nuevoTurno = {
        id: Date.now(),
        codigo: this.generarCodigo(datosTurno.servicio),
        servicio: datosTurno.servicio,
        nombre: datosTurno.nombre,
        documento: datosTurno.documento,
        horaSolicitud: new Date().toISOString(),
        atendido: false
      };

      this.turnos.unshift(nuevoTurno);
      return nuevoTurno;
    },

    marcarAtendido(id) {
      const turno = this.turnos.find(t => t.id === id);
      if (turno) {
        turno.atendido = true;
        turno.horaAtencion = new Date().toISOString();
      }
    }
  },
  persist: true
});
