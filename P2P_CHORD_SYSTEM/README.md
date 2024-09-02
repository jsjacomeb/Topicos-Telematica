# Sistema P2P con Microservicios para Compartir Archivos

## ST0263: Tópicos Especiales en Telemática, 2024-2
### Universidad EAFIT

**Estudiantes:** Juan Sebastian Jacome Burbano, Daniel Alberto Garcia Salcedo  
**Correos Electrónicos:** jsjacomeb@eafit.edu.co, dagarcias@eafit.edu.co  
**Profesor:** Alvaro Enrique Ospina San Juan, aeospinas@eafit.edu.co

### Descripción del Proyecto

Este proyecto implementa un sistema Peer-to-Peer (P2P) para la distribución de archivos de manera descentralizada, utilizando una arquitectura basada en microservicios. La solución emplea una red P2P estructurada mediante el protocolo Chord y una DHT (Tabla de Hash Distribuida) para la localización de archivos. Los nodos se comunican entre sí usando API REST, gRPC y un Middleware Orientado a Mensajes (MOM) utilizando RabbitMQ.

### Arquitectura del Sistema

El sistema está compuesto por los siguientes elementos:

1. **Nodos P2P:** Cada nodo opera simultáneamente como servidor y cliente, ejecutando microservicios que permiten compartir archivos.
2. **Portmapper:** Gestiona la lista de nodos presentes en la red, monitoreando su disponibilidad y facilitando la comunicación entre ellos.
3. **Microservicios:**
   - **Servicio DHT con gRPC:** Mantiene la estructura de la red P2P y maneja la localización de los archivos.
   - **Servicio de Indexación:** Proporciona una lista de los archivos disponibles en un nodo específico.
   - **Servicio de Subida de Archivos (Upload):** Facilita la subida de archivos a un nodo en la red.
   - **Servicio de Descarga de Archivos (Download):** Permite la descarga de archivos desde un nodo.
   - **Servicio MOM:** Gestiona la comunicación asíncrona entre los nodos usando RabbitMQ.

### Requisitos

- **Python 3.x** (versión recomendada)
- **RabbitMQ** (necesario para la gestión MOM)
- **Paquetes de Python necesarios:** 
  - `FastAPI` (v0.x.x)
  - `Uvicorn` (v0.x.x)
  - `pika` (v1.x.x) para la integración con RabbitMQ
  - `requests` (v2.x.x)
  - `multiprocessing` para el manejo de procesos en paralelo

### Instalación

1. Clona este repositorio en tu máquina local usando el siguiente comando:
    ```bash
    git clone https://github.com/jsjacomeb/reto1
    ```
2. Navega al directorio donde se encuentra el proyecto:
    ```bash
    cd tu_repositorio
    ```

### Uso

1. Configura las direcciones IP y puertos de los nodos en el archivo de configuración.
2. Inicia el servidor principal ejecutando el siguiente comando:

    ```bash
    python main.py
    ```

    Luego, abre una nueva terminal y ejecuta el siguiente comando para iniciar el portmapper:

    ```bash
    uvicorn portmapper:app --host 127.0.0.1 --port 8000
    ```

    Finalmente, abre otra terminal y ejecuta el cliente con el comando:

    ```bash
    python client.py
    ```

3. Utiliza el menú interactivo para buscar, subir y descargar archivos entre los nodos de la red.

### Información Adicional

- Asegúrate de que RabbitMQ esté en funcionamiento antes de arrancar el sistema para garantizar que el servicio de comunicación asíncrona funcione correctamente.
- Configura correctamente las IPs y los puertos en los archivos de configuración para evitar conflictos y asegurar una comunicación efectiva entre los nodos.

### Referencias

- [Guía de uso de RabbitMQ con pika en Python](https://pika.readthedocs.io/)
