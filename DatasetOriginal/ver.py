from datasets import load_dataset

def download_dataset():
    # Cargar el conjunto de datos
    ds = load_dataset("foduucom/table-detection-yolo", name="full")
    
    # Guardar el conjunto de datos localmente
    save_path = "C:/Users/ferna/OneDrive/Escritorio/MATERIAS/Human Perception in Computer Vision (MAR24-AGOS24)/Unidad 3/Deberes/PROYCETO/MODELO-PRACTICO/DatasetOriginal"
    ds.save_to_disk(save_path)

    print(f"¡El conjunto de datos se ha descargado y guardado correctamente en {save_path}!")

if __name__ == "__main__":
    download_dataset()
