from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from ultralytics import YOLO
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/ImagenesCargadas'
app.config['IMAGE_FOLDER'] = 'static/images'

model = YOLO('best.pt')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            if image:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(image_path)
                return render_template('index.html', uploaded_image=image.filename)
    return render_template('index.html')

@app.route('/classify/<filename>')
def classify(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    results = model.predict(image_path)

    # Asumiendo que results es una lista de objetos, debemos iterar sobre ellos
    for result in results:
        if hasattr(result, 'render'):  # Verifica si el objeto tiene un método 'render'
            result.render()
        else:
            print("El objeto de resultados no tiene el método 'render'.")
    
    # Guardar la imagen con anotaciones si es necesario
    result_path = os.path.join(app.config['IMAGE_FOLDER'], 'Processed', filename)
    if len(results) > 0 and hasattr(results[0], 'save'):
        results[0].save(path=result_path)

    return render_template('index.html', uploaded_image=filename, results_path='Processed/' + filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
