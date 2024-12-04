from typing import Any
import flet as ft
import webbrowser
import time
from api_back import apiBack

class UI:
    def __init__(self, ip: str) -> None:
        self.__page = None
        self.ip = ip

    def __call__(self, flet_page: ft.Page) -> Any:
        self.__page = flet_page
        self.__page.title = 'GatoDeck'
        self.__page.padding = 0
        self.__page.theme_mode = ft.ThemeMode.DARK
        self.__page.window_title_bar_hidden = True
        self.__page.window_bgcolor = ft.colors.TRANSPARENT
        self.__page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.__page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.__page.bgcolor = ft.colors.TRANSPARENT
        self.__page.window_width = 420
        self.__page.window_height = 535
        self.width_container = 400
        self.__page.add(
            ft.Container(
                content=ft.WindowDragArea(
                        ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text('Escanea el QR', color='black')
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                bgcolor='white',
                                width=self.width_container,
                                border_radius=ft.border_radius.all(10),
                                padding=5
                            ),
                            ft.Image(
                                src=f'http://localhost/static/qr.png',
                                width=self.width_container,
                                height=self.width_container,
                                fit=ft.ImageFit.CONTAIN,
                                border_radius=ft.border_radius.all(10)
                            ),
                            ft.ElevatedButton(
                                'Abrir GatoDeck',
                                on_click=lambda e: webbrowser.open(f'http://{self.ip}:8080'),
                                color='black',
                                bgcolor='white',
                                on_hover=lambda e: self.hover(e, 'green'),
                                width=self.width_container
                            ),
                            ft.ElevatedButton(
                                'Cerrar',
                                on_click=lambda e: e.page.window_destroy(),
                                color='black',
                                bgcolor='white',
                                on_hover=lambda e: self.hover(e, 'red'),
                                width=self.width_container
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
                bgcolor= '#00000000',
                opacity=1,
                alignment= ft.alignment.center,
                width=self.width_container,
            )
        )

    def hover(self, e, color):
        if e.data == 'true':
            e.control.bgcolor = color
            e.control.update()
        else:
            e.control.bgcolor = 'white'
            e.control.update()

def run_ui(ip):
    ui = UI(ip)
    time.sleep(3)
    ft.app(target=ui, assets_dir='static')