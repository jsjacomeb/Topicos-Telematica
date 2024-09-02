# info de la materia: ST0263-1716 Topicos Especiales en Telematica
#
# Estudiante(s): Jacome Burbano Juan Sebastian, jsjacomeb@eafit.edu.co
#                Garcia Salcedo Daniel Alberto, dagarcias@eafit.edu.co 
#
# Profesor: Alvaro Enrique Ospina San Juan, aeospinas@eafit.edu.co
#
# Reto 1
#
# 1. breve descripción de la actividad
Este proyecto consiste en un análisis de datos mediante técnicas de visualización y agrupación en Python. Se han utilizado bibliotecas como `pandas` y `matplotlib` para el análisis y representación gráfica de los datos.
## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
- Carga y procesamiento de datos desde archivos CSV.
- Agrupación de datos mediante la función `groupby`.
- Visualización de datos utilizando gráficos de barras y dispersión.
- Uso de bibliotecas estándar de Python para el análisis.
## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
- No se logro realizar el Docker y consigo conectarlo a un AWS Server

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
El proyecto sigue una estructura modular en la que las funciones se agrupan por tipo de tarea (procesamiento de datos, visualización). Además, se han seguido buenas prácticas en la nomenclatura de variables y funciones.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
**Lenguaje de Programación**: Python 3.x  
**Librerías y Paquetes Utilizados**:
- `pandas`
- `matplotlib`

### Compilación y Ejecución
Para ejecutar el proyecto, asegúrate de tener instaladas las librerías necesarias. Puedes instalarlas ejecutando:
    pip install pandas matplotlib

Luego, ejecuta el script principal:
    python main.py

# Detalles del Desarrollo
- El script carga un archivo CSV y agrupa los datos por categorías utilizando la función groupby.
- Se generan gráficos de barras y gráficos de dispersión para visualizar la relación entre las variables.

# Configuración de Parámetros del Proyecto
- El archivo de datos informacion.csv debe estar ubicado en la misma carpeta que el script Python.
- Asegúrate de que los datos estén en el formato correcto para evitar errores de lectura.
# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o Nombres de Dominio
 Como se informo anteriormente, esto fue lo que no se logro


# Configuración de Parámetros del Proyecto
No se requiere configuración adicional en el entorno de ejecución.

# Cómo Lanzar el Servidor
 Como se informo anteriormente, esto fue lo que no se logro

# Guía de Uso para Usuarios
- Los usuarios pueden ejecutar el script para obtener los gráficos de visualización de los datos proporcionados.
- Asegúrate de que el archivo CSV esté correctamente formateado y ubicado en la carpeta adecuada.

# 5. otra información que considere relevante para esta actividad.
Este proyecto está orientado a la visualización de datos de forma básica. Para análisis más profundos, se recomienda explorar técnicas adicionales como el modelado de datos y machine learning.

# Referencias
pandas Documentation: https://pandas.pydata.org/pandas-docs/stable/
matplotlib Documentation: https://matplotlib.org/stable/index.htm
