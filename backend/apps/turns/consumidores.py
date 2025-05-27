from channels.generic.websocket import AsyncWebsocketConsumer
import logging
logger = logging.getLogger(__name__)

class ConsumidorTurnos(AsyncWebsocketConsumer):

    async def connect(self):
        logger.info('Nueva conexión WebSocket')
        await self.accept()

    async def disconnect(self, close_code):
        logger.warning(f'Conexión cerrada: código {close_code}')

    async def receive(self, text_data):
        logger.debug(f'Mensaje recibido: {text_data}')
        # Eco simple para pruebas
        await self.send(text_data=f"Eco: {text_data}")
