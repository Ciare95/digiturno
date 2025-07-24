import axios from "axios";

const URL = "http://127.0.0.1:8000/api/";

/**
 * Obtiene la lista de sucursales desde la API.
 * @returns {Promise<[]>} Promesa que se resuelve con la lista de sucursales.
 * @throws {Error} Lanza un error si no se puede obtener la lista de sucursales.
 */
export async function obtenerSucursales() {
  const response = await fetch('/api/sucursales/');
  const text = await response.text();
  console.log('Respuesta cruda:', text);
  try {
    const data = JSON.parse(text);
    if (!data || !Array.isArray(data.results)) {
      throw new Error('La respuesta de la API no contiene un array de sucursales');
    }
    return data.results;
  } catch (e) {
    console.error('No se pudo parsear la respuesta como JSON:', text);
    throw e;
  }
}