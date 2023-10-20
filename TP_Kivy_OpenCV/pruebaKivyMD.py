from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.lang import Builder
import cv2
import datetime
from kivy.uix.image import AsyncImage
from kivy.graphics.texture import Texture
from google.protobuf.json_format import MessageToDict

KV = """
ScreenManager:
    IndexScreen:
        name: "index"
    CameraScreen:
        name: "camera"
    FileScreen:
        name: "files"

<IndexScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'

        BoxLayout:
            orientation: 'horizontal'
            spacing: '10dp'

            MDRaisedButton:
                text: 'Login'
                size_hint: None, None
                size: (150, 50)
                theme_text_color: 'Secondary'
                on_release: app.root.current = 'login'

            MDRaisedButton:
                text: 'Nuevo Usuario'
                size_hint: None, None
                size: (150, 50)
                theme_text_color: 'Secondary'

        BoxLayout:
            orientation: 'vertical'
            padding: '20dp'

            MDLabel:
                text: "Index"
                font_size: 24
                theme_text_color: "Secondary"

            BoxLayout:
                orientation: 'horizontal'
                spacing: '10dp'
                padding: '20dp'

                MDRaisedButton:
                    text: "Files"
                    size_hint: (None, None)
                    size: (150, 50)
                    theme_text_color: 'Secondary'
                    on_release: app.root.current = 'files'

                MDRaisedButton:
                    text: "Camera"
                    size_hint: (None, None)
                    size: (150, 50)
                    theme_text_color: 'Secondary'
                    on_release: app.root.current = 'camera'

<CameraScreen>:
    BoxLayout:
        orientation: 'vertical'

        MDLabel:
            text: "Cámara"
            font_size: 24
            theme_text_color: "Secondary"

        VideoPlayer:
            source: "your_video.mp4"

        MDRaisedButton:
            text: "<- Atrás"
            size_hint: (None, None)
            size: (150, 50)
            theme_text_color: 'Secondary'
            on_release: app.root.current = 'index'

<FileScreen>:
    BoxLayout:
        orientation: 'vertical'

        MDFileManager:
            id: file_manager
            path: '.'
            filters: ['*.jpg', '*.png', '*.mp4']

        BoxLayout:
            orientation: 'vertical'
            id: media_widget

        MDRaisedButton:
            text: "<- Atrás"
            size_hint: (None, None)
            size: (150, 50)
            theme_text_color: 'Secondary'
            on_release: app.root.current = 'index'
"""

class IndexScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Pantalla de inicio"
        layout = MDBoxLayout(orientation='vertical')
        label = MDLabel(text="Menú", halign='center')
        layout.add_widget(label)
        botones_layout = MDBoxLayout(orientation='horizontal', spacing=10, padding=[20, 20, 20, 20],
                                     size_hint=(1, None), height=50)

        boton_archivos = MDRaisedButton(text="Archivos", size=(100, 50))
        boton_archivos.bind(on_release=self.abrir_archivos)
        botones_layout.add_widget(boton_archivos)

        boton_camara = MDRaisedButton(text="Cámara", size=(100, 50))
        boton_camara.bind(on_release=self.abrir_camara)
        botones_layout.add_widget(boton_camara)

        layout.add_widget(botones_layout)
        self.add_widget(layout)

    def abrir_camara(self, instance):
        if "camera" not in self.manager.screen_names:
            self.manager.add_widget(CameraScreen(name="camera"))
        self.manager.current = "camera"

    def abrir_archivos(self, instance):
        self.manager.current = "files"

    def on_pre_enter(self):
        self.manager.current = "index"
        self.manager.transition.direction = 'right'
        self.title = "Pantalla de inicio"

class CameraScreen(Screen):
    cont_izq = 0
    cont_der = 0
    is_recording = False
    foto = False
    grabar_video = None
    frame_width = int(cv2.VideoCapture(3).get(3))
    frame_height = int(cv2.VideoCapture(3).get(4))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Camara"
        layout = MDBoxLayout(orientation='vertical')
        self.capture = cv2.VideoCapture(3)
        self.image = Image()
        layout.add_widget(self.image)
        self.label = MDLabel(text="", size_hint_y=None, height=50, halign='center')
        layout.add_widget(self.label)
        boton_indice = MDRaisedButton(text="<- Atrás", size_hint=(None, None), size=(100, 50))
        boton_indice.bind(on_release=self.go_to_index)
        layout.add_widget(boton_indice)
        self.add_widget(layout)
        self.capture = cv2.VideoCapture(3)

    def actualiza(self, dt):
        ret, frame = self.capture.read()
        if ret:
            img = self.capture
            img2 = cv2.flip(frame, 0).tostring()
            textura1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            textura1.blit_buffer(img2, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = textura1
            success, img = img.read()
            img = cv2.flip(img, 1)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(imgRGB)

            if results.multi_hand_landmarks:
                now = datetime.datetime.now()
                date_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
                if len(results.multi_handedness) == 2:
                    self.label.text = f"Ambas Manos Detectadas"
                    self.cont_der = 0
                    self.cont_izq = 0
                    if self.is_recording:
                        self.grabar_video.release()
                        self.is_recording = False
                else:
                    for i in results.multi_handedness:
                        mano = MessageToDict(i)['classification'][0]['label']
                        if mano == 'Left':
                            if self.cont_izq == 5 and not self.foto:
                                self.label.text = f"Capturando imágen, aguarde..."
                                cv2.imwrite(f"fotos_videos/imagen{date_time_str}.jpg", img)
                                self.foto = True
                            else:
                                self.label.text = f"Quedan {5 - self.cont_izq} segundos para capturar la imágen"

                        if mano == 'Right':
                            if self.cont_der >= 5:
                                self.label.text = f"Van {self.cont_der - 5} segundos de grabación"
                                if not self.is_recording:
                                    self.grabar_video = cv2.VideoWriter(f"fotos_videos/video{date_time_str}.mp4",
                                                                        cv2.VideoWriter_fourcc(*'XVID'), 20.0,
                                                                        (self.frame_width, self.frame_height))
                                    self.is_recording = True
                            else:
                                self.label.text = f"En {5 - self.cont_der} segundos comienza la grabación"
            else:
                self.label.text = f"Para iniciar la grabación de un video, mostrar la mano derecha.\nPara tomar una fotografía, mostrar la mano izquierda"
                self.cont_der = 0
                self.cont_izq = 0

            if self.is_recording:
                self.grabar_video.write(img)

    def on_pre_enter(self):
        MDApp.get_running_app().title = self.title

    def go_to_index(self, instance):
        self.manager.current = "index"

    def on_stop(self):
        self.capture.release()
        Clock.unschedule(self.actualiza)

class FileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Explorador de archivos"
        layout = MDBoxLayout(orientation='vertical')

        # Create MDFileManager instance without 'path' argument
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

        # Set the 'path' property after creating the instance
        self.file_manager.path = 'E:/Programs/Python/TP_Kivy_OpenCV/fotos_videos'  # Update this path to your desired folder

        layout.add_widget(self.file_manager)
        self.media_widget = MDBoxLayout(orientation='vertical')
        layout.add_widget(self.media_widget)
        boton_archivos = MDRaisedButton(
            text="<- Atrás",
            size_hint=(None, None),
            size=(150, 50),
        )
        boton_archivos.bind(on_release=self.abrir_index)
        layout.add_widget(boton_archivos)
        self.add_widget(layout)

    def select_path(self, path):
        self.exit_manager()
        self.cargar_archivos(None, [path])

    def cargar_archivos(self, instance, value):
        self.media_widget.clear_widgets()
        selected = value
        if selected:
            selected_file = selected[0]
            if selected_file.lower().endswith(('.jpg', '.png')):
                image_widget = AsyncImage(source=selected_file)
                self.media_widget.add_widget(image_widget)
            elif selected_file.lower().endswith('.mp4'):
                video_player = VideoPlayer(source=selected_file, state='play')
                self.media_widget.add_widget(video_player)

    def abrir_index(self, instance):
        self.manager.current = "index"

    def exit_manager(self, *args):
        self.manager_open = False
        Window.size = (400, 600)

    def on_pre_enter(self):
        self.title = "Explorador de archivos"
        Builder.load_file('indexxx.kv')

class MyApp(MDApp):
    def build(self):
        self.title = "Your App Title"  # Set the title of the application window
        sm = ScreenManager()
        sm.add_widget(IndexScreen(name="index"))
        sm.add_widget(CameraScreen(name="camera"))
        sm.add_widget(FileScreen(name="files"))
        return sm

if __name__ == '__main__':
    MyApp().run()
