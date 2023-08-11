from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.lang import Builder


class CustomBubbleButton(BubbleButton):
    pass


class NumericKeyboard(Bubble):
    layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(NumericKeyboard, self).__init__(**kwargs)
        self.create_bubble_button()

    def create_bubble_button(self):
        numeric_keypad = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '', '0', '.']
        for x in numeric_keypad:
            if len(x) == 0:
                self.layout.add_widget(Label(text=""))
            else:
                bubb_btn = CustomBubbleButton(text=str(x))
                self.layout.add_widget(bubb_btn)


class BubbleShowcase(FloatLayout):
    text_input = ObjectProperty(None)

    def show_bubble(self, *l):
        if not hasattr(self, 'bubb'):
            self.bubb = bubb = NumericKeyboard()
            self.bubb.arrow_pos = "bottom_mid"
            self.add_widget(bubb)


Builder.load_file("test.kv")


class TestBubbleApp(App):
    title = "Numeric Key Pad - Using Bubble"

    def build(self):
        return BubbleShowcase()


if __name__ == '__main__':
    TestBubbleApp().run()