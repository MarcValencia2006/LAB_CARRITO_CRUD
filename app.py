from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'upea_2026_key'

contactos_db = []
id_counter = 1

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
    if 'carrito' not in session:
        session['carrito'] = []

    if request.method == 'POST':
        producto = request.form['producto']
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])
        
        session['carrito'].append({
            'producto': producto,
            'precio': precio,
            'cantidad': cantidad,
            'total': precio * cantidad
        })
        session.modified = True
        return redirect(url_for('carrito'))

    gran_total = sum(item['total'] for item in session['carrito'])
    return render_template('carrito.html', carrito=session['carrito'], gran_total=gran_total)

@app.route('/limpiar_carrito')
def limpiar_carrito():
    session.pop('carrito', None)
    return redirect(url_for('carrito'))

@app.route('/contactos', methods=['GET', 'POST'])
def gestion_contactos():
    global id_counter
    if request.method == 'POST':
        contactos_db.append({
            'id': id_counter,
            'nombre': request.form['nombre'],
            'correo': request.form['correo'],
            'celular': request.form['celular']
        })
        id_counter += 1
        return redirect(url_for('gestion_contactos'))
    return render_template('contactos.html', contactos=contactos_db)

@app.route('/editar_contacto/<int:id>', methods=['GET', 'POST'])
def editar_contacto(id):
    contacto = next((c for c in contactos_db if c['id'] == id), None)
    if not contacto:
        return redirect(url_for('gestion_contactos'))

    if request.method == 'POST':
        contacto['nombre'] = request.form['nombre']
        contacto['correo'] = request.form['correo']
        contacto['celular'] = request.form['celular']
        return redirect(url_for('gestion_contactos'))

    return render_template('editar_contacto.html', contacto=contacto)

@app.route('/eliminar_contacto/<int:id>')
def eliminar_contacto(id):
    global contactos_db
    contactos_db = [c for c in contactos_db if c['id'] != id]
    return redirect(url_for('gestion_contactos'))

if __name__ == '__main__':
    app.run(debug=True)