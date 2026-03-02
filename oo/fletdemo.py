import flet as ft

class OKButton(ft.ElevatedButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class YIconButton(ft.IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hover_color = ft.Colors.PINK
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0)
        )


def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        input.value = str(int(input.value) - 1)

    def plus_click(e):
        input.value = str(int(input.value) + 1)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                YIconButton(ft.Icons.REMOVE, on_click=minus_click),
                input,
                YIconButton(ft.Icons.ADD, on_click=plus_click),
            ],
        )
    )

ft.run(main)