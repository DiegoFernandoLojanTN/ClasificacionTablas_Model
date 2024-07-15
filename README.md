# Detección de Tablas en Imágenes

## Descripción
Este proyecto tiene como objetivo detectar y clasificar tablas en imágenes, diferenciando entre tablas con bordes y sin bordes. Utiliza un modelo entrenado de Hugging Face para realizar el análisis y la evaluación de métricas. Además, se ha incorporado una interfaz utilizando Flask, ya que el modelo en la página de Hugging Face no cuenta con una API. Los usuarios pueden cargar una imagen, clasificarla y visualizar los resultados de manera intuitiva.

## Enlace al Modelo en Hugging Face
[Modelo de Detección de Tablas - Hugging Face](https://huggingface.co/foduucom/table-detection-and-extraction)

## Descripcion del Modelo
- El modelo YOLOv8s Table Detection sirve como una solución versátil para identificar precisamente tablas dentro de imágenes, ya sea que presenten un diseño con bordes o sin bordes. Además de la detección, este modelo juega un papel crucial en abordar las complejidades de los documentos no estructurados. Al emplear técnicas avanzadas como la delineación de cuadros delimitadores, el modelo permite a los usuarios aislar tablas de interés dentro del contenido visual.
- Lo que distingue a este modelo es su sinergia con la tecnología de Reconocimiento Óptico de Caracteres (OCR). Esta integración fluida empodera al modelo para no solo localizar tablas sino también extraer los datos pertinentes contenidos en ellas. La información de los cuadros delimitadores guía el recorte de tablas, lo que luego se combina con OCR para extraer meticulosamente los datos textuales, agilizando el proceso de recuperación de información de documentos no estructurados.

## Arquitectura
- **Frontend**: HTML, CSS, Bootstrap
- **Backend**: Flask (Python)
- **Técnica (CNN) de Detección**: YOLO (You Only Look Once)
- **Modelo de Detección**: Ultralytics YOLOv8

## Métricas
El modelo de detección de tablas YOLOv8s ha sido evaluado utilizando la métrica mAP (mean Average Precision) a un umbral de 0.5 para la intersección sobre la unión (IoU). Aquí están los resultados detallados:

- **mAP@0.5 (box)**: Esta métrica mide la precisión promedio del modelo a un umbral de IoU de 0.5. Indica la capacidad del modelo para detectar y clasificar correctamente las tablas dentro de las imágenes.
  - **All**: 0.962 -> 96.2%
    - Esta es la precisión promedio del modelo en la detección de todas las tablas, sin importar si son con bordes o sin bordes.
  - **Bordered**: 0.961 -> 96.1%
    - Esta es la precisión del modelo específicamente en la detección de tablas con bordes.
  - **Borderless**: 0.963 -> 96.3%
    - Esta es la precisión del modelo específicamente en la detección de tablas sin bordes.


## Herramientas de Trabajo
- **IDE**: Visual Studio Code
- **Lenguajes de Programación**: Python, HTML, CSS
- **Bibliotecas y Frameworks**:
  - Flask
  - Bootstrap
  - Font Awesome
  - Ultralytics YOLO

## Interfaz
La interfaz del usuario está diseñada para ser intuitiva y fácil de usar:
- **Carga de Imágenes**: Los usuarios pueden cargar imágenes desde su dispositivo.
- **Clasificación**: Después de cargar la imagen, los usuarios pueden clasificarla para detectar tablas con bordes o sin bordes.
- **Visualización**: Los resultados de la clasificación se muestran junto con la imagen original y la imagen clasificada.

## Resultados
- **Subida de Imagen**: Permite al usuario subir una imagen para su análisis.
- **Clasificación**: Detecta y clasifica las tablas en la imagen como con bordes o sin bordes.
- **Visualización**: Muestra la imagen original y la imagen procesada con las tablas detectadas y clasificadas.

## Ejemplo de Uso

1. **Ejemplo de Deteccipon**
   [![imagen-2024-07-15-112045252.png](https://i.postimg.cc/j5Ks8JWd/imagen-2024-07-15-112045252.png)](https://postimg.cc/2qcRyyFP)

## Licencia
Este proyecto está licenciado bajo la [MIT License](LICENSE).

