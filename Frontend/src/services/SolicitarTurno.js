import axios from "axios";

const API_URL = "http://192.168.2.4:8000/api/turns/";

export const solicitarTurno = async (turno) => {
    try {
        const response = await axios.post(API_URL + "turnos/", turno);
        return response.data;
    } catch (error) {
        console.error("Error al solicitar turno:", error);
        if (error.response) {
            console.error("Respuesta de error del backend:", error.response.data);
        }
        throw error;
    }
}

export const obtenerTurnos = async () => {
    try {
        const response = await axios.get(API_URL + "turnos/cola/");
        return response.data;
    } catch (error) {
        console.error("Error al obtener turnos:", error);
        throw error;
    }
}
