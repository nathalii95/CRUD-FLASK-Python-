from flask import Flask, redirect, request, url_for, render_template, session
#import mysql.connector
import basedatos

from config import config

#SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'
app = Flask(__name__)
app.secret_key = 'B!1w8NAt1T^%kvhUI*S^'  # Esto se usa para firmar las sesiones, cámbialo por una clave segura.
app.config.from_object(config['development'])  # Selecciona la configuración de desarrollo

#autenticacion



# Rutas para el inicio de sesión y autenticación
#@app.route('/')
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']
        if basedatos.verificar_credenciales(nombre_usuario, contraseña):
            session['usuario'] = nombre_usuario
            return redirect(url_for('inicio'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html', error=None)


@app.route('/inicio')
def inicio():
    if 'usuario' in session:
        return render_template('inicio.html', usuario=session['usuario'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))



#Insertar un articulo 
#@app.route('/agregar_articulo')
#def agregar_articulo(): #llamando al metodo la funcion bd.py
#return render_template('agregar-articulo.html') 

@app.route('/agregar_articulo')
def agregar_articulo():
    try:
        categorias = basedatos.listar_categorias()  # Llamando al método listar_categorias
    except Exception as e:
        print(f"Error al listar las categorías: {e}")
        categorias = []
    finally:
        return render_template('agregar-articulo.html', categorias=categorias)

#Guardar un articulo 
@app.route('/guardar_articulo', methods=['POST'])
def guardar_articulo():
    nombre= request.form['nombre']
    precio= request.form['precio']
    categoria= request.form['categoria']
    try:
        basedatos.insertar_articulo(nombre, precio, categoria) #llamando metodo insertar_articulo
    except Exception as e:
        print(f" Lo sentimos ha ocurrido un error desde insertar {e}")
    finally:
        return redirect('/articulos')




#Prsentación de la lista de articulos
@app.route('/articulos')
def articulos():
    try:
        articulos = basedatos.listar_articulos() #llamando al metodo listar_articulo
    except Exception as e:
        print(f"Ha ocurrido el error {e}")
    finally:
        return render_template('articulos.html', articulos=articulos)
                #renderizamos y asignamos la misma variables o alguna informacion

#Editar un articulo
@app.route('/editar_articulo/<int:id>')
def editar_articulo(id):
    try:
      articulo = basedatos.obtener_articulo(id)
      categorias = basedatos.listar_categorias()  # Llamando al método listar_categorias
    except Exception as e:
        print(f"No se ha encontrado el articulo : {e}")
    finally:
        return render_template('editar-articulo.html', articulo = articulo , categorias=categorias)



@app.route('/actualizar_articulo', methods=['POST'])
def actualizar_articulo():
    id = request.form['id']
    nombre= request.form['nombre']
    precio= request.form['precio']
    categoria= request.form['categoria']
    try:
        basedatos.actualizar_articulo(id,nombre, precio, categoria) #llamando y eviando metodo actualizar_articulo
    except Exception as e:
        print(f" Lo sentimos ha ocurrido un error desde actualizr el articulo {e}")
    finally:
        return redirect('/articulos')



#Elininar un articulo
@app.route('/eliminar_articulo', methods=['POST'])
def eliminar_articulo():
    try:
        basedatos.eliminar_articulo(request.form['id']) #llamando metodo insertar_articulo
    except Exception as e:
        print(f" Ha ocurrido un error, no se encuentra {e}")
    finally:
        return redirect('/articulos')
    

############## CATEGORIA


#Prsentación de la lista de categoria
@app.route('/categoria')
def categoria():
    try:
        categorias = basedatos.listar_categorias() #llamando al metodo listar_articulo
    except Exception as e:
        print(f"Ha ocurrido el error {e}")
    finally:
        return render_template('categoria.html', categorias=categorias)
                #renderizamos y asignamos la misma variables o alguna informacion

#Insertar un articulo link en el form html categoria
@app.route('/agregar_categoria')
def agregar_categoria(): #llamando al metodo la funcion bd.py
    return render_template('agregar-categoria.html') 

#Guardar un articulo 
@app.route('/guardar_categoria', methods=['POST'])
def guardar_categoria():
    nombre= request.form['nombre']
    try:
        basedatos.insertar_categorias(nombre) #llamando metodo insertar_articulo
    except Exception as e:
        print(f" Lo sentimos ha ocurrido un error desde insertar {e}")
    finally:
        return redirect('/categoria')



#Editar un categoria
@app.route('/editar_categoria/<int:id>')
def editar_categoria(id):
    try:
      articulo = basedatos.obtener_categoria(id)
      categorias = basedatos.listar_categorias()  # Llamando al método listar_categorias
    except Exception as e:
        print(f"No se ha encontrado el categoria : {e}")
    finally:
        return render_template('editar-categoria.html', articulo = articulo , categorias=categorias)



@app.route('/actualizar_categoria', methods=['POST'])
def actualizar_categoria():
    id = request.form['id']
    nombre= request.form['nombre']
    try:
        basedatos.actualizar_categoria(id,nombre) #llamando y eviando metodo actualizar_articulo
    except Exception as e:
        print(f" Lo sentimos ha ocurrido un error desde actualizr el categoria {e}")
    finally:
        return redirect('/categoria')



#Eliminar un categoria
@app.route('/eliminar_categoria', methods=['POST'])
def eliminar_categoria():
    try:
        basedatos.eliminar_categoria(request.form['id']) #llamando metodo insertar_articulo
    except Exception as e:
        print(f" Ha ocurrido un error, no se encuentra {e}")
    finally:
        return redirect('/categoria')
    

if __name__ == '__main__':
    app.run(debug=True)
