import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def fex(url, file_type, filter=None):
    """
    Extrae una lista de enlaces de archivos con extensiones especificadas de un sitio web,
    con la opción de filtrar los enlaces usando una expresión regular.

    Parámetros:
    - url (str): URL del sitio web a analizar.
    - file_type (list o str): Extensiones de archivos a buscar.
      Puede ser una lista ['xlsx', 'xls'] o un string 'xlsx'.
      Si se usa "all", buscará archivos de tipo xlsx, xls y csv.
    - filter (str o None): Expresión regular para filtrar la lista de URLs finales.

    Retorna:
    - list: Lista de enlaces absolutos a archivos con las extensiones seleccionadas y que cumplen el filtro.
    """
    response = requests.get(url)
    response.raise_for_status()  # Verificar si la solicitud fue exitosa
    soup = BeautifulSoup(response.text, 'html.parser')

    # Normalizar file_type para aceptar un string o una lista
    if isinstance(file_type, str):
        if file_type == "all":
            file_type = ['xlsx', 'xls', 'csv']  # Tipos de archivo considerados como datos
        else:
            file_type = [file_type]  # Convertirlo a lista si es un string único

    # Buscar todos los enlaces en la página
    links = soup.find_all('a', href=True)

    # Convertir enlaces relativos en absolutos y filtrar los archivos con las extensiones deseadas
    archivos = [urljoin(url, link['href']) for link in links if any(link['href'].lower().endswith(f".{ext}") for ext in file_type)]

    # Aplicar filtro si se proporciona
    if filter is not None:
        pattern = re.compile(filter, flags=re.IGNORECASE)
        archivos = [archivo for archivo in archivos if pattern.search(archivo)]

    # Mostrar un mensaje si no se encuentra ningún archivo del tipo solicitado
    if not archivos:
        tipo_mensaje = "los formatos: " + ", ".join(file_type)
        if filter:
            tipo_mensaje += f" y el filtro '{filter}'"
        print(f"No se encontraron archivos con {tipo_mensaje}")

    return archivos