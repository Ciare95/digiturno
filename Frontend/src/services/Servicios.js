import axios from "axios";

const url = "http://localhost:8000/api/";

export async function obtenerServicios() {
    const response = await axios.get(url + "servicios/");
    try {
        const data = response.data;
        if (!data || !Array.isArray(data.results)) {
            throw new Error('La respuesta de la API no contiene un array de servicios');
        }
        return data.results;
    } catch (error) {
        console.error("Error al obtener servicios:", error);
        throw error;
    }
}