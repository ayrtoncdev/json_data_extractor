import requests
from PIL import Image
from io import BytesIO
from requests.auth import HTTPBasicAuth
import json

# Configuración inicial de WooCommerce
WC_API_URL = ''
WC_CONSUMER_KEY = ''
WC_CONSUMER_SECRET = ''
AUTH = (WC_CONSUMER_KEY, WC_CONSUMER_SECRET)

# Configuración de WordPress para subida de imágenes
WP_USERNAME = ''
WP_PASSWORD = ''
WP_API_MEDIA_ENDPOINT = ''

def obtener_y_guardar_datos(url):
    # Hacemos una petición GET para obtener los datos
    respuesta = requests.get(url, auth=AUTH)
    
    # Verificamos si la petición fue exitosa
    if respuesta.status_code == 200:
        datos = respuesta.json()
        
        # Guardamos los datos en un archivo
        with open('datos.json', 'w') as archivo:
            json.dump(datos, archivo, indent=4)
        
        print("Datos guardados exitosamente en 'datos.json'.")
    else:
        print(f"Error al obtener los datos: {respuesta.status_code}")

# Ejecutar la función
#obtener_y_guardar_datos(WC_API_URL)


def obtener_todos_los_productos():
    productos = []  # Lista para almacenar todos los productos
    page = 1  # Iniciar en la página 1
    while True:
        # Construir el endpoint para la página actual
        endpoint = f"{WC_API_URL}products?per_page=50&page={page}"
        respuesta = requests.get(endpoint, auth=AUTH)
        
        # Verificar si la petición fue exitosa
        if respuesta.status_code == 200:
            datos = respuesta.json()
            if not datos:
                # Si no hay más datos (lista vacía), romper el bucle
                break
            productos.extend(datos)
            page += 1  # Prepararse para solicitar la siguiente página
        else:
            print(f"Error al obtener los productos: {respuesta.status_code}")
            break
    
    # Opcional: Guardar los productos en un archivo JSON
    with open('productos.json', 'w') as archivo:
        json.dump(productos, archivo, indent=4)
    
    print(f"Total de productos obtenidos: {len(productos)}")

# Ejecutar la función
#obtener_todos_los_productos()


def extraer_datos_relevantes_del_archivo():
    # Abrir y leer los datos del archivo 'productos.json'
    try:
        with open('productos.json', 'r') as archivo:
            productos = json.load(archivo)
    except FileNotFoundError:
        print("El archivo 'productos.json' no se encontró.")
        return

    # Extraer solo los datos relevantes de cada producto
    productos_resumidos = [
        {"id": producto["id"], "name": producto["name"], "permalink": producto["permalink"], "images": producto["images"]}
        for producto in productos
    ]
    
    # Guardar los productos resumidos en un archivo JSON
    with open('productos_resumidos.json', 'w') as archivo:
        json.dump(productos_resumidos, archivo, indent=4)
    
    print(f"Total de productos resumidos guardados: {len(productos_resumidos)}")

# Ejecutar la función
#extraer_datos_relevantes_del_archivo()


def extraer_datos_relevantes_con_imagenes():
    # Abrir y leer los datos del archivo 'productos.json'
    try:
        with open('productos.json', 'r') as archivo:
            productos = json.load(archivo)
    except FileNotFoundError:
        print("El archivo 'productos.json' no se encontró.")
        return

    productos_resumidos = []
    for producto in productos:
        # Extraer las URLs de las imágenes
        urls_imagenes = [imagen['src'] for imagen in producto.get('images', [])]

        # Crear el diccionario del producto resumido incluyendo las imágenes
        producto_resumido = {
            "id": producto["id"],
            "name": producto["name"],
            "permalink": producto["permalink"],
            "images": urls_imagenes  # Lista de URLs de las imágenes
        }
        
        productos_resumidos.append(producto_resumido)
    
    # Guardar los productos resumidos en un nuevo archivo JSON
    with open('productos_final.json', 'w') as archivo:
        json.dump(productos_resumidos, archivo, indent=4)
    
    print(f"Total de productos resumidos con imágenes guardados: {len(productos_resumidos)}")

# Ejecutar la función
#extraer_datos_relevantes_con_imagenes()


def extraer_datos_relevantes_con_detalle_imagenes():
    # Abrir y leer los datos del archivo 'productos.json'
    try:
        with open('productos.json', 'r') as archivo:
            productos = json.load(archivo)
    except FileNotFoundError:
        print("El archivo 'productos.json' no se encontró.")
        return

    productos_resumidos = []
    for producto in productos:
        # Extraer los detalles necesarios de las imágenes
        imagenes_detalladas = [
            {"id": imagen['id'], "src": imagen['src']}
            for imagen in producto.get('images', [])
        ]

        # Crear el diccionario del producto resumido incluyendo las imágenes detalladas
        producto_resumido = {
            "id": producto["id"],
            "name": producto["name"],
            "permalink": producto["permalink"],
            "images": imagenes_detalladas  # Lista de objetos de imágenes con id y src
        }
        
        productos_resumidos.append(producto_resumido)
    
    # Guardar los productos resumidos en un nuevo archivo JSON
    with open('productos_final2.json', 'w') as archivo:
        json.dump(productos_resumidos, archivo, indent=4)
    
    print(f"Total de productos resumidos con detalle de imágenes guardados: {len(productos_resumidos)}")

# Ejecutar la función
#extraer_datos_relevantes_con_detalle_imagenes()