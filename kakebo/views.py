from kakebo import app
from flask import jsonify, render_template, request #El jsonify es un json dumps con esteroides.
from kakebo.forms import MovimientosForm
import sqlite3

@app.route('/')
def index():
    conexion = sqlite3.connect("movimientos.db") #Creamos la conexion con el servidor
    cur = conexion.cursor() #El cursor es como la herramienta que viajará en la conexion
    cur.execute("SELECT * FROM movimientos;") #Cursor recopila la información en la db en movimientos

    claves = cur.description
    filas = cur.fetchall() #cursor me devuelve la informacion
    movimientos = []
    saldo = 0

    for fila in filas:
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
            print(d)
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo
        movimientos.append(d)

    conexion.close()

    return render_template('movimientos.html', datos = movimientos)



@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm()

    if request.method == 'GET':
        return render_template('alta.html', form = formulario)
    else:

        if formulario.validate():
            conexion = sqlite3.connect("movimientos.db")
            cur = conexion.cursor()

            #Consulta a la base de datos
            query = "INSERT INTO movimientos VALUES (fecha, concepto, categoria, esGasto, cantidad) (?, ?, ?, ?, ?)"
            try:
                cur.execute(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                            formulario.esGasto.data, formulario.cantidad.data])
            except sqlite3.Error as el_error:
                print("Error en SQL INSERT", el_error)
                return render_template('alta.html', form = formulario)


            """
            query = "INSERT INTO movimientos VALUES (fecha, concepto, categoria, esGasto, cantidad) (:fecha, :concepto, :categoria, :esGasto, :cantidad)"
            cur.execute(query, {
                'fecha': formulario.fecha.data, 
                'concepto': formulario.concepto.data, 
                'categoria': formulario.categoria.data,
                'esGasto': formulario.esGasto.data, 
                'cantidad':formulario.cantidad.data
            }
            """

            conexion.commit() #El cambio realizado lo fija en la base de datos
            conexion.close()
            #Redirect a la ruta /
        else:
            return render_template('alta.html', form = formulario)

