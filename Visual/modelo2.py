import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session
from werkzeug.utils import secure_filename
from ultralyticsplus import YOLO, render_result
from PIL import Image

# Configuración de Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/output'
app.config['MODEL2_FOLDER'] = 'static/modelo2'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clave secreta para sesiones

# Crear carpetas si no existen
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
os.makedirs(app.config['MODEL2_FOLDER'], exist_ok=True)

# Crear subcarpetas de salida
bordered_dir = os.path.join(app.config['MODEL2_FOLDER'], 'bordered')
borderless_dir = os.path.join(app.config['MODEL2_FOLDER'], 'borderless')
failed_dir = os.path.join(app.config['MODEL2_FOLDER'], 'Failed')

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        session['last_uploaded_image'] = filename  # Guardar la última imagen cargada en sesión
        return render_template('upload.html', filename=filename)
    return redirect(request.url)

@app.route('/classify/<filename>')
def classify_image(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Realizar la inferencia
    results = model.predict(filepath)

    # Verificar las detecciones
    if len(results[0].boxes) == 0:
        # No se detectó nada
        save_path = os.path.join(failed_dir, filename)
        result_message = "No se detectaron tablas en la imagen."
        result_image = None
    else:
        # Se detectaron objetos
        detected_class = results[0].boxes[0].cls[0].item()
        if detected_class == 0:  # Clase 0: bordered
            save_path = os.path.join(bordered_dir, filename)
            result_message = "Se detectó una tabla con borde en la imagen."
        elif detected_class == 1:  # Clase 1: borderless
            save_path = os.path.join(borderless_dir, filename)
            result_message = "Se detectó una tabla sin borde en la imagen."
        else:
            # Si hay otras clases, por ahora tratémoslas como fallidas
            save_path = os.path.join(failed_dir, filename)
            result_message = "No se pudo clasificar correctamente la imagen."
    
    # Guardar la imagen renderizada
    render = render_result(model=model, image=filepath, result=results[0])
    render.save(save_path)
    
    # Ruta de la imagen renderizada para mostrar en la plantilla
    if os.path.exists(save_path):
        result_image = os.path.join('modelo2', os.path.basename(save_path))
        session['last_classified_image'] = result_image  # Guardar la ruta de la última imagen clasificada en sesión
    
    return render_template('upload.html', filename=filename, result_message=result_message, result_image=result_image)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/load_last_classified_image')
def load_last_classified_image():
    result_image = session.get('last_classified_image', None)
    if result_image:
        return render_template('upload.html', result_image=result_image)
    else:
        return "No hay una imagen clasificada recientemente."

if __name__ == "__main__":
    app.run(debug=True)
