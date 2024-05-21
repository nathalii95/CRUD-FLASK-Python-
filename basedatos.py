import pymysql

def dame_conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        port=3306,
        password='',
        db='base-flask')

def insertar_articulo(nombre, precio, categoria):
    conexion = dame_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO articulos(nombre,precio,id_categoria) VALUES (%s, %s,%s)", (nombre, precio,categoria))
         #metodo que ejecute el sql    %S(indica los valores de formulario)       parametros enviados desde el metodo
        conexion.commit() #una actualizacion
        conexion.close()  #asi como abro , cierro la ejecucion

def listar_articulos():
    conexion = dame_conexion()
    articulos = [] #creamos lista vacia
    with conexion.cursor() as cursor: #cursor selecionamos algo
        #cursor.execute("SELECT id, nombre, precio, id_categoria FROM articulos") """
        cursor.execute("SELECT p.id, p.nombre, p.precio, p.id_categoria, c.nombre FROM articulos p JOIN categoria c ON p.id_categoria = c.id")
        articulos = cursor.fetchall()
        conexion.close()
        return articulos

#actualizar
#trae el articulo
def obtener_articulo(id):
    conexion = dame_conexion()
    articulo = None
    with conexion.cursor() as cursor: #cursor selecionamos algo
            #cursor.execute("SELECT id,nombre,precio, id_categoria FROM articulos WHERE id =%s", (id))
            cursor.execute("SELECT p.id, p.nombre, p.precio, p.id_categoria, c.nombre as categoria FROM articulos p JOIN categoria c ON p.id_categoria = c.id WHERE p.id =%s", (id))    
            articulo = cursor.fetchone()
            conexion.close()  #asi como abro , cierro la ejecucion
            return articulo
    
#actualizar el producto por id
def actualizar_articulo(id, nombre, precio, categoria):
    conexion = dame_conexion()
    with conexion.cursor() as cursor: #cursor selecionamos algo
            cursor.execute("UPDATE articulos SET nombre = %s, precio = %s, id_categoria = %s WHERE id =%s", (nombre, precio, categoria, id))
            conexion.commit()
            conexion.close()  #asi como abro , cierro la ejecucion  

#eliminar
def eliminar_articulo(id):
        conexion = dame_conexion()
        with conexion.cursor() as cursor: #cursor selecionamos algo
            cursor.execute("DELETE FROM articulos WHERE id =%s", (id))
            conexion.commit() #una actualizacion
            conexion.close()  #asi como abro , cierro la ejecucion


##########CATEGORIA######

def listar_categorias():
    conexion = dame_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre FROM categoria")
        categorias = cursor.fetchall()
        conexion.close()
    return categorias


def insertar_categorias(nombre):
    conexion = dame_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO categoria(nombre) VALUES (%s)", (nombre))
         #metodo que ejecute el sql    %S(indica los valores de formulario)       parametros enviados desde el metodo
        conexion.commit() #una actualizacion


#actualizar el producto por id
def actualizar_categoria(id, nombre):
    conexion = dame_conexion()
    with conexion.cursor() as cursor: #cursor selecionamos algo
            cursor.execute("UPDATE categoria SET nombre = %s  WHERE id =%s", (nombre, id))
            conexion.commit()
            conexion.close()  #asi como abro , cierro la ejecucion  

def obtener_categoria(id):
    conexion = dame_conexion()
    categoria = None
    with conexion.cursor() as cursor: #cursor selecionamos algo
            cursor.execute("SELECT id,nombre FROM categoria WHERE id =%s", (id))
            categoria = cursor.fetchone()
            conexion.close()  #asi como abro , cierro la ejecucion
            return categoria
    

#eliminar
def eliminar_categoria(id):
        conexion = dame_conexion()
        with conexion.cursor() as cursor: #cursor selecionamos algo
            cursor.execute("DELETE FROM categoria WHERE id =%s", (id))
            conexion.commit() #una actualizacion
            conexion.close()  #asi como abro , cierro la ejecucion


#usuario
def verificar_credenciales(nombre_usuario, contraseña):
    try:
        conexion = dame_conexion()
        with conexion.cursor() as cursor:
            query = "SELECT COUNT(*) FROM usuarios WHERE nombre = %s AND contrasena = %s"
            cursor.execute(query, (nombre_usuario, contraseña))
            resultado = cursor.fetchone()
            if resultado[0] == 1:
                return True
            else:
                return False
    except Exception as e:
        print(f"Error al verificar credenciales: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

if __name__ == '__main__':
    dame_conexion()

