import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fex(url, file_type, filter_and=None, filter_or=None):
    """
    Extrae una lista de enlaces de archivos con extensiones especificadas de un sitio web,
    con la opción de filtrar los enlaces usando condiciones AND/OR sobre listas de palabras clave.

    Parámetros:
    - url (str): URL del sitio web a analizar.
    - file_type (list o str): Extensiones de archivos a buscar.
      Puede ser una lista ['xlsx', 'xls'] o un string 'xlsx'.
      Si se usa "all", buscará archivos de tipo xlsx, xls y csv.
    - filter_and (list o None): Lista de palabras clave. El enlace debe contener *todas* estas palabras.
    - filter_or (list o None): Lista de palabras clave. El enlace debe contener *al menos una* de estas palabras.

    Retorna:
    - list: Lista de enlaces absolutos a archivos con las extensiones seleccionadas y que cumplen los filtros.
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    if isinstance(file_type, str):
        if file_type == "all":
            file_type = ['xlsx', 'xls', 'csv']
        else:
            file_type = [file_type]

    links = soup.find_all('a', href=True)
    archivos = [
        urljoin(url, link['href']) 
        for link in links 
        if any(link['href'].lower().endswith(f".{ext}") for ext in file_type)
    ]

    def cumple_and(archivo, keywords):
        return all(palabra.lower() in archivo.lower() for palabra in keywords)

    def cumple_or(archivo, keywords):
        return any(palabra.lower() in archivo.lower() for palabra in keywords)

    if filter_and:
        archivos = [a for a in archivos if cumple_and(a, filter_and)]
    if filter_or:
        archivos = [a for a in archivos if cumple_or(a, filter_or)]

    if not archivos:
        mensaje = f"los formatos: {', '.join(file_type)}"
        if filter_and:
            mensaje += f" con todas las palabras {filter_and}"
        if filter_or:
            mensaje += f" con al menos una de las palabras {filter_or}"
        print(f"No se encontraron archivos con {mensaje}")

    return archivos