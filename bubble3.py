from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.base import EventLoop
from kivy.uix.textinput import TextInput


Config.set('input', 'mouse', 'mouse,disable_multitouch')

class RightClickTextInput(TextInput):
    def on_touch_down(self, touch):
        super(RightClickTextInput, self).on_touch_down(touch)
        if touch.button == 'right':
            print("Right mouse clicked")
            pos = touch.pos  # Get the position of the touch event
            self._show_cut_copy_paste(pos, EventLoop.window, mode='paste')

kv_string = Builder.load_string("""
RightClickTextInput:
    use_bubble: True
    text: 'Selecciona este texto o escribe un texto propio para utilizar el widget'
    multiline: True
    #readonly: True
""")

class MyApp(App):
    def build(self):
        return kv_string

if __name__ == '__main__':
    MyApp().run()