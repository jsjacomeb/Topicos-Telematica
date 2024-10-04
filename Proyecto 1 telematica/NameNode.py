import os

class NameNode:
    def __init__(self):
        self.datanodes = []  # Lista de datanodes registrados
        self.files_metadata = {}  # Metadata de archivos: nombre de archivo -> [(block_id, datanode_id)]
        self.block_registry = {}  # Registro de bloques: block_id -> [datanode_id]

    def register_datanode(self, node_id, storage_path):
        """Registra un nuevo Datanode y su ubicación de almacenamiento."""
        datanode = {
            "node_id": node_id,
            "storage_path": storage_path,
            "blocks": []  # Lista de bloques almacenados en este datanode
        }
        self.datanodes.append(datanode)
        print(f"Datanode {node_id} registrado con storage path: {storage_path}")

    def divide_and_distribute_file(self, file_name, file_data, replication_factor=2):
        """Divide un archivo en bloques y distribuye los bloques entre los datanodes."""
        block_size = 1 * 1024 * 1024  # 1 MB por bloque, para pruebas
        blocks = [file_data[i:i + block_size] for i in range(0, len(file_data), block_size)]
        block_locations = []

        print(f"Total blocks to distribute: {len(blocks)}")  # Depuración: número de bloques creados

        for i, block in enumerate(blocks):
            block_id = f"{file_name}_block_{i}"
            selected_datanodes = []

            # Selecciona los datanodes para replicación (simple round-robin)
            for j in range(replication_factor):
                datanode = self.datanodes[(i + j) % len(self.datanodes)]
                block_path = os.path.join(datanode["storage_path"], block_id)
                
                try:
                    with open(block_path, 'wb') as block_file:
                        block_file.write(block)
                    
                    # Actualiza la metadata
                    datanode["blocks"].append(block_id)
                    selected_datanodes.append(datanode["node_id"])
                    self.register_block(block_id, datanode["node_id"])
                    print(f"Block {block_id} stored in {datanode['node_id']} at {block_path}")  # Depuración
                except Exception as e:
                    print(f"Failed to store block {block_id} in {datanode['node_id']}: {e}")

            block_locations.append((block_id, selected_datanodes))

        # Almacena la metadata del archivo
        self.files_metadata[file_name] = block_locations
        return block_locations




    def register_block(self, block_id, datanode_id):
        """Registra la ubicación de un bloque en un Datanode."""
        if block_id not in self.block_registry:
            self.block_registry[block_id] = []
        self.block_registry[block_id].append(datanode_id)

    def get_file_blocks(self, file_name):
        """Devuelve la lista de bloques y su ubicación para un archivo dado."""
        if file_name in self.files_metadata:
            return self.files_metadata[file_name]
        else:
            return None

    def list_datanodes(self):
        """Muestra todos los datanodes registrados y los bloques que contienen."""
        for datanode in self.datanodes:
            print(f"Datanode {datanode['node_id']} con bloques: {datanode['blocks']}")
