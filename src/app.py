from flask import Flask, render_template, request, redirect, url_for
import os
import database as db


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,'src','templates')



app = Flask(__name__, template_folder=template_dir)



# rutas de la aplicacion
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute('SELECT * FROM users')
    myresult = cursor.fetchall()
    #convertir a diccionario
    insertObject = []
    columnName = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnName, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#ruta para guardar usuarios en la base de datos
@app.route('/user', methods=['POST'])
def addUser():
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']


    if username and name and password:
        cursor = db.database.cursor()
        cursor.execute('INSERT INTO users (username, name, password) VALUES (%s, %s, %s)', (username, name, password))
        db.database.commit()
        cursor.close()
    return redirect(url_for('home'))


#ruta para eliminar usuarios de la base de datos

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    cursor.execute('DELETE FROM users WHERE id = {0}'.format(id))
    db.database.commit()
    cursor.close()
    return redirect(url_for('home'))

#ruta para actualizar usuarios de la base de datos
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        cursor.execute('UPDATE users SET username = %s, name = %s, password = %s WHERE id = %s', (username, name, password, id))
        db.database.commit()
        cursor.close()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
