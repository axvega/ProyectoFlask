from flask import Flask, render_template, request, abort
import json
import os

app = Flask(__name__)

# Obtener la ruta absoluta del directorio del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'animales.json')

# Cargar datos desde el archivo JSON
try:
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        animales_data = data['animales']
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {JSON_PATH}")
    animales_data = []
except KeyError:
    print("Error: La clave 'animales' no existe en el JSON")
    animales_data = []

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para búsqueda y lista de animales
@app.route('/animales', methods=['GET', 'POST'])
def animales():
    search_query = ''
    tipo_query = ''
    tipos = sorted(list(set(animal['tipo'] for animal in animales_data)))
    
    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()
        tipo_query = request.form.get('tipo', '')
    
    # Crear lista de tuplas (animal, index)
    animales_con_indices = [(animal, index) for index, animal in enumerate(animales_data)]
    
    # Filtrar animales
    filtered_animales = animales_con_indices
    if search_query:
        filtered_animales = [(animal, index) for animal, index in filtered_animales 
                           if animal['nombre'].lower().startswith(search_query.lower())]
    if tipo_query:
        filtered_animales = [(animal, index) for animal, index in filtered_animales 
                           if animal['tipo'] == tipo_query]
    
    return render_template('animales.html', 
                         animales=filtered_animales, 
                         search_query=search_query, 
                         tipo_query=tipo_query, 
                         tipos=tipos)

# Ruta para detalle de un animal
@app.route('/animal/<int:id>')
def animal_detail(id):
    if id < 0 or id >= len(animales_data):
        abort(404)
    animal = animales_data[id]
    return render_template('animal_detail.html', animal=animal)

if __name__ == '__main__':
    app.run(debug=True)