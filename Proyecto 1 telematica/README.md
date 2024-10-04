# Proyecto de Sistema de Archivos Distribuido


## Integrantes
- Juan Sebastian Jacome
- Daniel Garcia Salcedo

**Universidad:** EAFIT  
**Materia:** Tópicos de Telemática

## Descripción

Este proyecto implementa un sistema de archivos distribuido (DFS) que permite almacenar, distribuir, y recuperar archivos en múltiples nodos (`Datanodes`). El sistema utiliza un `NameNode` para gestionar la metadata y coordinar la distribución de los bloques de archivos en los Datanodes. Los clientes pueden interactuar con el sistema utilizando una interfaz simple para cargar (`put`), descargar (`get`), y gestionar archivos.

## Arquitectura del Proyecto

El sistema se compone de los siguientes componentes principales:

- **Cliente:** Permite a los usuarios interactuar con el sistema mediante comandos como `put`, `get`, `mkdir`, `cd`, `ls`, y `rm`.
- **Servidor:** Recibe las solicitudes del cliente, interactúa con el `NameNode` para gestionar la metadata, y coordina la distribución y recuperación de archivos en los Datanodes.
- **NameNode:** Mantiene la metadata de los archivos, incluyendo información sobre la ubicación de los bloques en los Datanodes. Gestiona la división de archivos en bloques y coordina su almacenamiento.
- **Datanodes:** Almacenan los bloques individuales de los archivos distribuidos. Cada Datanode es un contenedor de almacenamiento para los bloques.

## Instalación

### Requisitos

- Python 3.x
- Conexión de red local o direccionamiento IP válido para la comunicación entre el cliente y el servidor.
- Carpetas de almacenamiento para los Datanodes.

### Configuración

1. Clona el repositorio o descarga los archivos del proyecto.
2. Asegúrate de que las siguientes carpetas de almacenamiento existen en el directorio del proyecto:
    ```bash
    mkdir datanode1_storage
    mkdir datanode2_storage
    mkdir datanode3_storage
    ```
3. Ejecuta el servidor en una terminal:
    ```bash
    python test_server.py
    ```
4. Ejecuta el cliente en otra terminal:
    ```bash
    python client.py
    ```

## Uso

### Comandos Disponibles

#### 1. `register`
- Registra un nuevo usuario en el sistema.
- **Sintaxis:** 
    ```
    register <username> <password>
    ```

#### 2. `login`
- Inicia sesión con un usuario existente.
- **Sintaxis:** 
    ```
    login <username> <password>
    ```

#### 3. `put`
- Carga un archivo desde el cliente al sistema distribuido.
-  
    ```
    put <file_name>
    ```
- 

#### 4. `get`
- Descarga un archivo del sistema distribuido al cliente.
- 
    ```
    get <file_name>
    ```
-

#### 5. `mkdir`
- Crea un directorio en el directorio actual del usuario.
- 
    ```
    mkdir <folder_name>
    ```

#### 6. `cd`
- Cambia al directorio especificado.
- 
    ```
    cd <folder_name>
    ```

#### 7. `ls`
- Lista los archivos y directorios en el directorio actual.
- 
    ```
    ls
    ```

#### 8. `rm`
- Elimina un archivo en el directorio actual.
-  
    ```
    rm <file_name>
    ```

#### 9. `rmdir`
- Elimina un directorio en el directorio actual.
- 
    ```
    rmdir <folder_name>
    ```

### Ejemplo de Flujo de Uso

1. Ejecuta el servidor:
    ```bash
    python test_server.py
    ```
2. Ejecuta el cliente y registra un nuevo usuario:
    ```
    Enter a command: register user1 password123
    ```
3. Inicia sesión:
    ```
    Enter a command: login user1 password123
    ```
4. Carga un archivo al sistema distribuido:
    ```
    Enter a command: put testfile.txt
    ```
5. Descarga el archivo al cliente:
    ```
    Enter a command: get testfile.txt
    ```

## Estructura del Código

- **`client.py`:** Contiene la lógica del cliente para interactuar con el servidor utilizando sockets.
- **`test_server.py`:** Implementa el servidor que coordina las operaciones de almacenamiento, recuperación y gestión de archivos.
- **`NameNode.py`:** Implementa la clase `NameNode` que mantiene la metadata de los archivos y gestiona la división y distribución de bloques.
- **Datanodes:** Carpetas (`datanode1_storage`, `datanode2_storage`, etc.) que almacenan los bloques de archivos.

## Características Técnicas

- **División en Bloques:** Los archivos se dividen en bloques de un tamaño fijo (configurable) antes de ser almacenados en los Datanodes.
- **Replicación:** Los bloques se replican en múltiples Datanodes para asegurar la redundancia y tolerancia a fallos.
- **Metadata:** El `NameNode` mantiene un registro centralizado de dónde se encuentra cada bloque, facilitando las operaciones de recuperación (`get`).
