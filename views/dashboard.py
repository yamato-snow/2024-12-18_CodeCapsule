import flet as ft
from utils.aging import calculate_aging_effect
from models.store import CapsuleStore
import logging

class Dashboard(ft.View):
    def __init__(self, store: CapsuleStore, page: ft.Page):
        super().__init__(route="/dashboard")
        self.store = store
        self.page = page

    def build(self):
        logging.info("Dashboard ビューの build メソッドが呼び出されました。")
        try:
            self.header = ft.Text(
                "CodeCapsule",
                size=40,
                font_family="RobotoMono",
                weight=ft.FontWeight.BOLD
            )
            
            self.test_text = ft.Text("Dashboard が正しくビルドされています。", size=20)

            self.new_button = ft.ElevatedButton(
                "新規作成",
                on_click=self.new_capsule,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            )

            capsules = self.store.get_all_capsules()
            logging.info(f"表示するキャプセル数: {len(capsules)}")

            capsule_cards = [
                self.create_capsule_card(capsule) for capsule in capsules
            ]
            self.capsules_list = ft.ListView(
                expand=True,
                spacing=10,
                padding=20,
                controls=capsule_cards
            )

            content = ft.Column([
                self.header,
                self.test_text,
                self.new_button,
                self.capsules_list
            ], spacing=10, expand=True)

            return content
        except Exception as e:
            logging.error(f"Dashboard.build でエラーが発生しました: {e}")
            return ft.Text("エラーが発生しました。")

    def new_capsule(self, e):
        logging.info("新規キャプセル作成ボタンがクリックされました。")
        self.page.go("/create")

    def create_capsule_card(self, capsule):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        capsule.message[:50] + "..." if len(capsule.message) > 50 else capsule.message,
                        size=16,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Text(f"作成日: {capsule.created_at.strftime('%Y-%m-%d')}", size=14),
                    ft.Text(f"コードの長さ: {len(capsule.code)}文字", size=14)
                ], spacing=5),
                padding=10,
                bgcolor="#424242",
                border_radius=10,
                on_click=lambda e: self.page.go(f"/view/{capsule.id}")
            )
        ) 