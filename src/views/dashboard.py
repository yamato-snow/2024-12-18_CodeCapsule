import flet as ft
from datetime import datetime
from utils.aging import calculate_aging_effect

class Dashboard(ft.UserControl):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def build(self):
        self.header = ft.Text(
            "CodeCapsule",
            size=40,
            font_family="RobotoMono",
            weight=ft.FontWeight.BOLD
        )
        
        self.new_button = ft.ElevatedButton(
            "新規作成",
            on_click=self.new_capsule,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            )
        )

        self.capsules_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
        )

        return ft.Column([
            self.header,
            self.new_button,
            self.capsules_list
        ])

    def new_capsule(self, e):
        self.page.go("/create")

    def create_capsule_card(self, capsule):
        effects = calculate_aging_effect(capsule.created_at)
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(capsule.message[:50] + "..."),
                    ft.Text(f"作成日: {capsule.created_at:%Y-%m-%d}"),
                    ft.Text(f"開封日: {capsule.open_at:%Y-%m-%d}")
                ]),
                padding=10,
                **effects
            ),
            on_click=lambda e: self.view_capsule(capsule.id)
        )