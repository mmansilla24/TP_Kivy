import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class AppBubble(App):
    def build(self):
        self.root = FloatLayout()
        button = Button(text= 'Presiona para mostrar la burbuja.', on_press = self.mostrar_bubble)
        self.root.add_widget(button)
        return self.root
    def mostrar_bubble(self, obj):
        bubble = Bubble(orientation = "horizontal",
                        size_hint = (None, None),
                        size = (100,100),
                        pos_hint = {'center_x': .5, 'center_y': .6})
        layout = BoxLayout(orientation='vertical')
        button1 = BubbleButton(text='Cortar')
        button2 = BubbleButton(text='Copiar')
        button3 = BubbleButton(text='Pegar')
        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)
        bubble.add_widget(layout)
        self.root.add_widget(bubble)

if __name__ == '__main__':
    AppBubble().run()