from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.filechooser import FileChooserListView
from DetectorManos import CameraScreen
from PantallaInicial import PantallaIngreso
from kivy.lang import Builder

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Pantalla de inicio"
        layout = BoxLayout(orientation='vertical')
        label = Label(text='[font=Bahamas.TTF][color=148F77][b]Menú[/b][/color][/font]', font_size='100sp', markup=True)
        label2 = Label(text='[font=Poppins-Regular.OTF][b]Explorador de Archivos:[/b] Presionar para ver las últimas capturas\n'
                            '\n[b]Cámara:[/b] presionar para tomar una fotografía o hacer una grabación[/font]',
                            font_size='20sp', halign='left', valign='top',markup=True)
        layout.add_widget(label)
        layout.add_widget(label2)
        botones_layout = BoxLayout(orientation='vertical', spacing=5, padding = [50, 35, 50, 35])
        boton_archivos = Button(text="[font=Poppins-Bold.OTF]Explorador de Archivos[/font]", size=(50, 50), font_size='20sp',markup=True)

        boton_archivos.bind(on_press=self.abrir_archivos)
        botones_layout.add_widget(boton_archivos)
        boton_camara = Button(text="[font=Poppins-Bold.OTF]Camara[/font]", size=(50, 50), font_size='20sp',markup=True)

        boton_camara.bind(on_press=self.abrir_camara)
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
        App.get_running_app().title = self.title

class FileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Explorador de archivos"
        layout = BoxLayout(orientation='vertical')
        self.file_chooser = FileChooserListView(path='.', filters=['*.jpg', '*.png', '*.mov'])
        layout.add_widget(self.file_chooser)
        self.media_widget = BoxLayout(orientation='vertical')
        layout.add_widget(self.media_widget)
        boton_archivos = Button(text="Atrás", size_hint=(None, None), size = (100, 50))
        boton_archivos.bind(on_press=self.abrir_menu)
        layout.add_widget(boton_archivos)
        self.add_widget(layout)
        self.file_chooser.bind(selection=self.cargar_archivos)

    def cargar_archivos(self, instance, value):
        self.media_widget.clear_widgets()
        selected = value
        if selected:
            selected_file = selected[0]
            if selected_file.lower().endswith(('.jpg', '.png')):
                image_widget = Image(source=selected_file)
                self.media_widget.add_widget(image_widget)
            elif selected_file.lower().endswith('.mov'):
                video_player = VideoPlayer(source=selected_file, state='play')
                self.media_widget.add_widget(video_player)

    def abrir_menu(self, instance):
        self.manager.current = "index"

    def on_pre_enter(self):
        App.get_running_app().title = self.title

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PantallaIngreso(name="login"))
        sm.add_widget(MenuScreen(name="index"))
        sm.add_widget(FileScreen(name="files"))
        return sm

if __name__ == '__main__':
    MyApp().run()
