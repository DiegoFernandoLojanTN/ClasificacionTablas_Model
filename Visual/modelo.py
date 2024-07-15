import os
from ultralyticsplus import YOLO, render_result
from PIL import Image

# Crear la estructura de carpetas si no existe
output_dir = 'SalidaDetecciones'
bordered_dir = os.path.join(output_dir, 'bordered')
borderless_dir = os.path.join(output_dir, 'borderless')
failed_dir = os.path.join(output_dir, 'Failed')

os.makedirs(bordered_dir, exist_ok=True)
os.makedirs(borderless_dir, exist_ok=True)
os.makedirs(failed_dir, exist_ok=True)

# Cargar el modelo
model = YOLO('foduucom/table-detection-and-extraction')

# Establecer parámetros del modelo
model.overrides['conf'] = 0.05  # Umbral de confianza para NMS
model.overrides['iou'] = 0.2  # Umbral IoU para NMS
model.overrides['agnostic_nms'] = False  # NMS no es agnóstico de clase
model.overrides['max_det'] = 1000  # Número máximo de detecciones por imagen

# Lista de imágenes a procesar
images = [
    'C:/Users/ferna/OneDrive/Escritorio/MATERIAS/Human Perception in Computer Vision (MAR24-AGOS24)/Unidad 3/Deberes/PROYCETO/MODELO-PRACTICO/Visual/images/1.png',
    'C:/Users/ferna/OneDrive/Escritorio/MATERIAS/Human Perception in Computer Vision (MAR24-AGOS24)/Unidad 3/Deberes/PROYCETO/MODELO-PRACTICO/Visual/images/2.png',
    'C:/Users/ferna/OneDrive/Escritorio/MATERIAS/Human Perception in Computer Vision (MAR24-AGOS24)/Unidad 3/Deberes/PROYCETO/MODELO-PRACTICO/Visual/images/3.png'
]

for image in images:
    # Realizar la inferencia
    results = model.predict(image)

    # Verificar las detecciones
    if len(results[0].boxes) == 0:
        # No se detectó nada
        save_path = os.path.join(failed_dir, os.path.basename(image))
    else:
        # Se detectaron objetos
        detected_class = results[0].boxes[0].cls[0].item()
        if detected_class == 0:  # Clase 0: bordered
            save_path = os.path.join(bordered_dir, os.path.basename(image))
        elif detected_class == 1:  # Clase 1: borderless
            save_path = os.path.join(borderless_dir, os.path.basename(image))
        else:
            # Si hay otras clases, por ahora tratémoslas como fallidas
            save_path = os.path.join(failed_dir, os.path.basename(image))
    
    # Guardar la imagen renderizada
    render = render_result(model=model, image=image, result=results[0])
    render.save(save_path)
    print(f"Imagen guardada en: {save_path}")
