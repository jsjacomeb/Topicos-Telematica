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
Este proyecto implementa un sistema P2P (peer-to-peer) para la gestión de archivos, donde varios nodos de una red pueden buscar, descargar y subir archivos. El sistema también soporta una cola de mensajes para gestionar peticiones en caso de que los nodos no estén activos.
## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
- Implementación de un sistema P2P con múltiples nodos.
- Funcionalidades de búsqueda, descarga y subida de archivos en la red P2P.
- Gestión de nodos activos e inactivos con soporte de cola de mensajes.
- Uso de FastAPI para la creación de microservicios REST.
- Implementación de servicios gRPC para la comunicación entre nodos.
- Configuración de colas de mensajes usando RabbitMQ.
## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
- La implementación del balanceo de carga entre nodos no fue completada.
- No se implementaron mecanismos avanzados de seguridad para las comunicaciones entre nodos.
- No se logro realizar el Docker y consigo conectarlo a un AWS Server

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
El diseño del sistema sigue una arquitectura basada en microservicios donde cada nodo es responsable de gestionar su propio conjunto de archivos. El sistema utiliza una combinación de REST y gRPC para la comunicación entre nodos. Además, se implementó una cola de mensajes (MOM) con RabbitMQ para gestionar peticiones a nodos inactivos.

### Patrones utilizados:

- **Microservicios**: Cada nodo actúa como un servicio independiente.
- **Message Queue**: Uso de colas para manejar tareas cuando los nodos no están disponibles.
- **Cliente-Servidor**: Implementación de servidores REST y gRPC en cada nodo.
  
# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
- **Lenguaje de programación**: Python 3.x
- **Librerías y paquetes**:
  - `FastAPI` (v0.x.x)
  - `Uvicorn` (v0.x.x)
  - `requests` (v2.x.x)
  - `pika` (v1.x.x) para la integración con RabbitMQ
  - `multiprocessing` para la ejecución de procesos en paralelo

### Cómo se compila y ejecuta

1. Clona el repositorio y navega al directorio del proyecto.
2. Instala las dependencias listadas en `requirements.txt`:
   ```bash
   pip install -r requirements.txt
3. Configura los nodos en el archivo de configuración correspondiente, incluyendo las direcciones IP y los puertos.
4. Para iniciar los nodos, ejecuta el siguiente comando:
      ```bash
       python main.py
##Detalles técnicos
- Cada nodo tiene una dirección IP y un puerto específicos configurados en el código.
- Los nodos se conectan entre sí mediante gRPC y REST.
- El sistema gestiona automáticamente los nodos inactivos utilizando RabbitMQ para encolar las peticiones que serán procesadas cuando el nodo vuelva a estar activo.

##Configuración de parámetros del proyecto
- IP y puertos: Configurados en el código, asegúrate de que no haya conflictos de puertos.
- Conexión a RabbitMQ: Asegúrate de tener RabbitMQ corriendo en localhost.
# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
- Lenguaje de programación: Python 3.x
- Librerías y paquetes:
    - 'FastAPI'
    - 'Uvicorn'
    - 'pika'
    - 'requests'
##Cómo se lanza el servidor
Para iniciar los nodos en producción, ejecuta el script principal que inicia los servicios REST, gRPC y MOM en paralelo:
      ```bash
       python main.py
##Mini guía de uso
1. Buscar y descargar un archivo:
    - Ejecuta la opción 1 en el menú interactivo del cliente, ingresa el nombre del archivo y sigue las instrucciones.
2. Subir un archivo:
    - Ejecuta la opción 2 en el menú, selecciona el nodo de destino y sigue las instrucciones.
3. Ver todos los nodos disponibles:
    - Ejecuta la opción 3 para listar los nodos activos e inactivos.
# 5. otra información que considere relevante para esta actividad.
Es importante asegurarse de que todos los nodos estén correctamente configurados y que RabbitMQ esté corriendo antes de ejecutar el sistema.

# Referencias
Documentación de FastAPI: https://fastapi.tiangolo.com/
RabbitMQ en Python con pika: https://pika.readthedocs.io/
