import sqlite3

class Data():
    #con = None
    def __init__(self):
        self.con = sqlite3.connect("comercio.db")
        self.crear_tabla_producto()

    def crear_tabla_producto(self):
        c = self.con.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS productos(
                    id_producto INTEGER,
                    nombre VARCHAR NOT NULL,
                    descripcion VARCHAR NOT NULL,
                    precio REAL NOT NULL,
                    stock INT NOT NULL,
                    PRIMARY KEY(id_producto))""")

    def agregar_producto(self, nombre, desc, precio, stock):
        c = self.con.cursor()
        c.execute("INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (?,?,?,?)",(nombre, desc, precio, stock))
        self.con.commit()
        return c.lastrowid

    def buscar_producto(self, prod_id):
        c = self.con.cursor()
        c.execute("SELECT * FROM productos WHERE id_producto = ?", (prod_id,))
        producto = c.fetchone()
        return producto

    def borrar_producto(self, prod_id):
        c = self.con.cursor()
        c.execute("DELETE FROM productos WHERE id_producto = ?", (prod_id,))
        self.con.commit()
        return c.rowcount

    def actualizar_producto(self, prod_id, nombre, desc, precio, stock):
        c = self.con.cursor()
        c.execute("UPDATE productos SET nombre=?, descripcion=?, precio=?, stock=? WHERE id_producto = ?",(nombre, desc, precio, stock, prod_id))
        self.con.commit()
        return c.rowcount

    def obtener_productos(self):
        c = self.con.cursor()
        c.execute("SELECT * FROM productos")
        productos = c.fetchall()
        return productos
        c.execute("UPDATE productos SET nombre=?, descripcion=?, precio=?, stock=? WHERE id_producto = ?",(nombre, desc, precio, stock, prod_id))
        self.con.commit()
        return c.rowcount

    def obtener_productos(self):
        c = self.con.cursor()
        c.execute("SELECT * FROM productos")
        productos = c.fetchall()
        return productos
