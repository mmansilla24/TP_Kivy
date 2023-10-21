from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import mediapipe as mp
import time
from threading import Thread
import datetime
from google.protobuf.json_format import MessageToDict
from kivy.uix.screenmanager import Screen

class CameraScreen(Screen):
    cont_izq = 0
    cont_der = 0
    is_recording = False
    foto = False
    grabar_video = None
    frame_width = int(cv2.VideoCapture(1).get(3))
    frame_height = int(cv2.VideoCapture(1).get(4))
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Camara"
        layout = BoxLayout(orientation='vertical')
        self.capture = cv2.VideoCapture(1)
        self.image = Image()
        layout.add_widget(self.image)
        self.label = Label(text="", size_hint_y=None, height=50)
        layout.add_widget(self.label)
        boton_indice = Button(text="[font=Poppins-Bold.OTF]Atrás[/font]", size_hint=(None, None), size = (100, 50), markup = True)
        boton_indice.bind(on_press=self.go_to_index)
        layout.add_widget(boton_indice)
        temporizador = Thread(target=self.fun_temporizador)
        temporizador.daemon = True
        temporizador.start()
        Clock.schedule_interval(self.actualiza, 1.0 / 30.0)

        self.add_widget(layout)

    def fun_temporizador(self):
        while True:
            time.sleep(1)
            self.cont_der += 1
            self.cont_izq += 1
            if self.cont_izq == 6:
                self.cont_izq = 0
                self.foto = False

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
                    self.label.text = f"[font=Poppins-Regular.OTF]Ambas Manos Detectadas[/font]"
                    self.label.markup = True
                    self.label.font_size= '20sp'
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
                                self.label.text = f"[font=Poppins-Regular.OTF]Capturando imágen, aguarde...[/font]"
                                self.label.markup = True
                                self.label.font_size = '20sp'
                                cv2.imwrite(f"fotos_videos/imagen{date_time_str}.jpg", img)
                                self.foto = True
                            else:
                                self.label.text = f"[font=Poppins-Regular.OTF]Quedan {5 - self.cont_izq} segundos para capturar la imágen[/font]"
                                self.label.markup = True
                                self.label.font_size = '20sp'
                            
                        if mano == 'Right':
                            if self.cont_der >= 5:
                                self.label.text = f"[font=Poppins-Regular.OTF]Van {self.cont_der - 5} segundos de grabación[/font]"
                                self.label.markup = True
                                self.label.font_size = '20sp'
                                if not self.is_recording:
                                    self.grabar_video = cv2.VideoWriter(f"fotos_videos/video{date_time_str}.mov", cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (self.frame_width, self.frame_height))
                                    if not self.grabar_video.isOpened():
                                        print("Error: Could not open video file for writing.")
                                    else:
                                        self.is_recording = True
                                    #self.is_recording = True
                            else:
                                self.label.text = f"[font=Poppins-Regular.OTF]En {5 - self.cont_der} segundos comienza la grabación[/font]"
                                self.label.markup = True
                                self.label.font_size = '20sp'
            else:
                self.label.text = f"[font=Poppins-Regular.OTF]Para iniciar la grabación de un video, mostrar la mano derecha.\nPara tomar una fotografía, mostrar la mano izquierda.[/font]"
                self.label.markup = True
                self.label.font_size = '20sp'
                self.cont_der = 0
                self.cont_izq = 0

            if self.is_recording:
                self.grabar_video.write(img)

    def on_pre_enter(self):
        App.get_running_app().title = self.title

    def go_to_index(self, instance):
        self.manager.current = "index"

    def on_stop(self):
        self.capture.release()
        Clock.unschedule(self.actualiza)

