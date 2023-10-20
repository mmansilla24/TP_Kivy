import cv2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import datetime
import os
from deepface import DeepFace

class PantallaIngreso(Screen):
    log_in = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Ingreso"
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="[font=Bahamas.TTF][b]Registro de ingreso[/b][/font]", size_hint_y=None, height=45, font_size='36sp', markup=True)
        layout.add_widget(self.label)
        self.capture = cv2.VideoCapture(3)
        self.image = Image()
        layout.add_widget(self.image)
        botones_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), height=50, padding=10,
                                  pos_hint={'center_x': 0.40})

        boton_login = Button(text="[font=Poppins-Bold.OTF]Ingresar[/font]", size_hint=(None, None), size=(110, 50), font_size='15sp', markup=True)
        boton_login.bind(on_press=self.validar_captura)
        botones_layout.add_widget(boton_login)

        boton_login = Button(text="[font=Poppins-Bold.OTF]Crear Usuario[/font]", size_hint=(None, None), size=(110, 50), font_size='15sp', markup = True)
        boton_login.bind(on_press=self.crear_usuario)
        botones_layout.add_widget(boton_login)
        layout.add_widget(botones_layout)
        Clock.schedule_interval(self.actualiza, 1.0 / 30.0)
        self.add_widget(layout)

    def actualiza(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            buffer = cv2.flip(frame, 0).tostring()
            textura1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            textura1.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = textura1

        if self.log_in:
            print("Ingreso")
            self.on_stop()
            self.abrir_index()

    def validar_identidad(self):
        carpeta_imagenes = "rostros"
        archivos = os.listdir(carpeta_imagenes)
        rostro_referencia = "captura.jpg"
        print("Validando Identidad...")
        for archivo in archivos:
            imagen_actual = os.path.join(carpeta_imagenes, archivo)
            try:
                validacion = DeepFace.verify(img1_path=rostro_referencia, img2_path=imagen_actual)["verified"]
                if validacion:
                    print("Usuario Valido.")
                    return True
            except Exception as e:
                print(f"Usuario no coincide con {archivo}")
        print("Usuario no encontrado")
        return False

    def validar_captura(self, instance):
        self.label.text = "Validando identidad..."
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite("captura.jpg", frame)
            print("Imagen capturada y guardada como 'captura.jpg'")

        try:
            self.log_in = self.validar_identidad()
            if not self.log_in:
                self.label.text = f"Usuario no encontrado."
        except Exception as e:
            print(e)

    def crear_usuario(self, instance):
        now = datetime.datetime.now()
        date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite(f"rostros/{date_time_str}.jpg", frame)
            self.label.text = f"Usuario registrado correctamente."
            print("Usuario registrado correctamente.")

    def abrir_index(self):
        self.manager.current = "index"

    def on_pre_enter(self):
        App.get_running_app().title = self.title

    def on_stop(self):
        self.capture.release()
        Clock.unschedule(self.actualiza)
