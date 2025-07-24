import axios from "axios";

const url = "http://127.0.0.1:8000/api/";

export const solicitarTurno = async (turno) => {
    try {
        const response = await axios.post(url + "turnos/", turno);
        return response.data;
    } catch (error) {
        console.error("Error al solicitar turno:", error);
        throw error;
    }
}

export const obtenerTurnos = async () => {
    try {
        const response = await axios.get(url + "turnos/");
        return response.data;
    } catch (error) {
        console.error("Error al obtener turnos:", error);
        throw error;
    }
}