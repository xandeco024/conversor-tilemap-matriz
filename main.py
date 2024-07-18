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

    view = ft.Row(
        width="100%",
        height="100%",

        controls = [
            ft.Column(
                width="20%",
                height="100%",
                controls = [
                    ft.Container(
                        width="100%",
                        height="100%",
                        bgcolor="lightgray",
                        content = [
                            AseTxtBtn("New"),
                            AseTxtBtn("Open"),
                            AseTxtBtn("Save"),
                            AseTxtBtn("Export"),
                            ]
                        )
                    ]
                ),
            ft.Container(
                width="80%",
                height="100%",
                )
            ]
        )

    #page.add(toolsContainer)
    page.add(view)

ft.app(main)