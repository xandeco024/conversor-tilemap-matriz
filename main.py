import flet as ft

class AseTxtBtn(ft.ElevatedButton):
    def __init__(self, text):
        super().__init__(text)
        self.text = text
        self.border_radius = 0

    def on_click(self):
        print("Clicked", self.text)

def ToolsContainer():
    pass

def main(page: ft.Page):
    
    page.title = "Pygas"

    controls = [
        toolsContainer = ft.Container(
            width=200,
            height=1000,
            bgcolor="red",
            margin=0,
        ),

        mainContainer = ft.Container(
            width="100",
            height="100",
            bgcolor="blue",
            margin=0,
        ),
    ]

    #page.add(toolsContainer)
    page.add(controls)

ft.app(main)