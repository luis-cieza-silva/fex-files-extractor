# fex

**fex** (files extractor) es una función en Python que permite encontrar y extraer directamente los enlaces a archivos de datos (.xlsx, .xls o .csv) desde cualquier página web, sin necesidad de descargar manualmente cada archivo.

## ¿Para qué sirve?

Muchas veces, para acceder a datos públicos o informes de páginas web, es necesario descargar los archivos uno por uno, lo cual puede ser tedioso y lento.  
**fex** automatiza este proceso: analiza la página web, identifica los archivos disponibles, y entrega una lista de enlaces directos que puedes usar para descargar o trabajar con esos archivos de forma inmediata.

### Beneficios principales

- Ahorra tiempo al evitar descargas manuales.
- Facilita el acceso masivo a datos abiertos o documentos.
- Permite integrar la extracción de archivos en flujos de trabajo automáticos.
- Hace más eficientes proyectos de análisis de datos o recolección de información.

## ¿Cómo funciona?

El script busca archivos en la página web que terminen en las extensiones que indiques (`xlsx`, `xls`, `csv`).  
Además, puedes usar filtros opcionales para encontrar archivos que contengan ciertas palabras clave, ya sea que **todas deban estar presentes** (`filter_and`) o **solo alguna** (`filter_or`).

## Requisitos

- Python 3
- Librerías:
  - `requests`
  - `beautifulsoup4`

Puedes instalar las librerías necesarias ejecutando:

```bash
pip install requests beautifulsoup4
```

## Uso

```python
from fex import fex

# Extraer todos los archivos .xlsx de una página
urls = fex("https://ejemplo.com/descargas", "xlsx")

# Extraer todos los archivos .xlsx, .xls y .csv
urls = fex("https://ejemplo.com/descargas", "all")

# Extraer archivos .csv que contengan al menos una de las palabras clave
urls = fex("https://ejemplo.com/descargas", "csv", filter_or=["2024", "enero"])

# Extraer archivos .xls que contengan todas las palabras clave
urls = fex("https://ejemplo.com/descargas", "xls", filter_and=["boletin", "2023"])

# Filtrar por AND y OR al mismo tiempo (se aplican en cascada)
urls = fex("https://ejemplo.com/descargas", "all", filter_and=["regional", "enero"], filter_or=["2023", "2024"])

print(urls)
```


## Parámetros

| Parámetro    | Tipo             | Descripción                                                                                                                                                               |
| ------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`        | `str`            | URL de la página web donde buscar archivos.                                                                                                                               |
| `file_type`  | `str` o `list`   | Extensiones de archivo a buscar. Puede ser un texto como `'xlsx'` o una lista como `['xlsx', 'csv']`. También puedes usar `'all'` para buscar todos los formatos comunes. |
| `filter_and` | `list`, opcional | Lista de palabras clave. Se filtran solo los archivos que contienen **todas** esas palabras.                                                                              |
| `filter_or`  | `list`, opcional | Lista de palabras clave. Se conservan los archivos que contienen **al menos una** de esas palabras.                                                                       |
## Ejemplo sencillo

Imagina que en una página hay varios archivos, pero tú solo quieres los que mencionan **"Reporte"** y **"2024"** en el nombre. Puedes usar:

```python
fex("https://ejemplo.com/descargas", "xlsx", filter_and=["reporte", "2024"])
````
Y obtendrás directamente los enlaces que cumplen ambas condiciones.
