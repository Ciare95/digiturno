import sys
import locale
import psycopg2

# Configuración de codificación
print(f"Python version: {sys.version}")
print(f"Default encoding: {sys.getdefaultencoding()}")
print(f"Filesystem encoding: {sys.getfilesystemencoding()}")
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

try:
    conn = psycopg2.connect(
        dbname='digiturno'.encode('ascii').decode('utf-8'),
        user='postgres'.encode('ascii').decode('utf-8'),
        password='postgres'.encode('ascii').decode('utf-8'),
        host='localhost'.encode('ascii').decode('utf-8'),
        port='5432'.encode('ascii').decode('utf-8'),
        client_encoding='UTF8'
    )
    print("¡Conexión exitosa!")
    conn.close()
except Exception as e:
    print(f"Error de conexión: {str(e)}")
    print(f"Tipo de error: {type(e).__name__}")
    print(f"Codificación actual: {locale.getpreferredencoding()}")
