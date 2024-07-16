import flet as ft

class AseTxtBtn(ft.ElevatedButton):
    def __init__(self, text):
        super().__init__(text)
        self.text = text
        self.border_radius = 0

    def on_click(self):
        print("Clicked", self.text)

def main(page: ft.Page):
    
    btn = AseTxtBtn("Click me")
    btn2 = ft.ElevatedButton("Click me")
    page.add(btn)
    page.add(btn2)

    page.add(ft.SafeArea(ft.Text("Hello, Flet!")))


ft.app(main)