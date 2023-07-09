import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from data import Data
from kivy.config import Config


Config.set('graphics','width',400) # defino el tamaño de los botones
Config.set('graphics','height',200)

class Contenedor_01(BoxLayout): # Solo crea una ventana (widget) contenedora de contenido, por el momento, vacía
    def __init__(self, **kwargs):
        super(Contenedor_01, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.data = Data()

        # Etiquetas y campos de entrada para los datos del producto
        self.lbl_id = Label(text="ID:")
        self.txt_id = TextInput()
        self.lbl_nombre = Label(text="Nombre:")
        self.txt_nombre = TextInput()
        self.lbl_desc = Label(text="Descripción:")
        self.txt_desc = TextInput()
        self.lbl_precio = Label(text="Precio:")
        self.txt_precio = TextInput()
        self.lbl_stock = Label(text="Stock:")
        self.txt_stock = TextInput()

        # Botones de acciones
        self.btn_agregar = Button(text="Agregar", on_release=self.agregar_producto)
        self.btn_buscar = Button(text="Buscar", on_release=self.buscar_producto)
        self.btn_actualizar = Button(text="Actualizar", on_release=self.actualizar_producto)
        self.btn_borrar = Button(text="Borrar", on_release=self.borrar_producto)

        # Área de mensajes
        self.lbl_mensaje = Label()

        # Contenedor principal
        self.contenedor = BoxLayout(orientation="vertical", spacing=10, size_hint=(None, None))
        self.contenedor.bind(minimum_height=self.contenedor.setter('height'))

        # Scrollview para la lista de productos
        self.scrollview = ScrollView(size_hint=(1, 0.7), do_scroll_x=False)
        self.scrollview.add_widget(self.contenedor)

        # Agregar los widgets a la interfaz
        self.add_widget(self.lbl_id)
        self.add_widget(self.txt_id)
        self.add_widget(self.lbl_nombre)
        self.add_widget(self.txt_nombre)
        self.add_widget(self.lbl_desc)
        self.add_widget(self.txt_desc)
        self.add_widget(self.lbl_precio)
        self.add_widget(self.txt_precio)
        self.add_widget(self.lbl_stock)
        self.add_widget(self.txt_stock)
        self.add_widget(self.btn_agregar)
        self.add_widget(self.btn_buscar)
        self.add_widget(self.btn_actualizar)
        self.add_widget(self.btn_borrar)
        self.add_widget(self.scrollview)
        self.add_widget(self.lbl_mensaje)

        # Cargar la lista de productos al iniciar
        self.cargar_productos()

    def cargar_productos(self):
        self.contenedor.clear_widgets()
        productos = self.data.obtener_productos()
        for producto in productos:
            item = BoxLayout(orientation="horizontal", spacing=10, size_hint=(1, None), height=30)
            item.add_widget(Label(text=str(producto[0])))
            item.add_widget(Label(text=producto[1]))
            item.add_widget(Label(text=producto[2]))
            item.add_widget(Label(text=str(producto[3])))
            item.add_widget(Label(text=str(producto[4])))
            self.contenedor.add_widget(item)

    def agregar_producto(self, *args):
        nombre = self.txt_nombre.text
        desc = self.txt_desc.text
        precio = float(self.txt_precio.text)
        stock = int(self.txt_stock.text)

        if nombre and desc and precio and stock:
            self.data.agregar_producto(nombre, desc, precio, stock)
            self.cargar_productos()
            self.lbl_mensaje.text = "Producto agregado exitosamente."
        else:
            self.mostrar_mensaje_error("Todos los campos son requeridos.")

    def mostrar_mensaje_error(self, mensaje):
        popup = Popup(title="Error", content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()

    def buscar_producto(self, *args):
        id_producto = int(self.txt_id.text)

        if id_producto:
            producto = self.data.buscar_producto(id_producto)
            if producto:
                self.txt_nombre.text = producto[1]
                self.txt_desc.text = producto[2]
                self.txt_precio.text = str(producto[3])
                self.txt_stock.text = str(producto[4])
                self.lbl_mensaje.text = ""
            else:
                self.mostrar_mensaje_error("Producto no encontrado.")
        else:
            self.mostrar_mensaje_error("Ingrese el ID del producto a buscar.")

    def actualizar_producto(self, *args):
        id_producto = int(self.txt_id.text)
        nombre = self.txt_nombre.text
        desc = self.txt_desc.text
        precio = float(self.txt_precio.text)
        stock = int(self.txt_stock.text)

        if id_producto and nombre and desc and precio and stock:
            self.data.actualizar_producto(id_producto, nombre, desc, precio, stock)
            self.cargar_productos()
            self.lbl_mensaje.text = "Producto actualizado exitosamente."
        else:
            self.mostrar_mensaje_error("Todos los campos son requeridos.")

    def borrar_producto(self, *args):
        id_producto = int(self.txt_id.text)

        if id_producto:
            self.data.borrar_producto(id_producto)
            self.cargar_productos()
            self.lbl_mensaje.text = "Producto borrado exitosamente."
        else:
            self.mostrar_mensaje_error("Debes ingresar un ID de producto válido.")


class MainApp(App): #Esta tiene que tener el mismo nombre que el archivo .kv
    title = 'TP kivy'
    def build(self): # Obligatoria agregarla, pq es lo primero que va a buscar
        return Contenedor_01()

if __name__ == '__main__':
    MainApp().run()
