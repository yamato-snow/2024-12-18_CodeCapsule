import flet as ft
import logging
from models.store import CapsuleStore
from views.dashboard import Dashboard
from views.editor import CapsuleEditor
from views.viewer import CapsuleViewer

class MainLayout:
    def __init__(self, page: ft.Page):
        self.page = page
        self.navbar = ft.Row(
            [
                ft.TextButton("ダッシュボード", on_click=lambda _: page.go("/dashboard")),
                ft.TextButton("新規作成", on_click=lambda _: page.go("/create")),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20
        )

    def get_layout(self, content):
        return ft.Column([
            self.navbar,
            content
        ], expand=True)

def main(page: ft.Page):
    # ログ設定
    logging.basicConfig(level=logging.DEBUG)
    
    page.title = "CodeCapsule"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1000
    page.window.height = 800
    
    store = CapsuleStore()
    layout = MainLayout(page)
    
    def route_change(e: ft.RouteChangeEvent):
        try:
            logging.info(f"Route changed to: {e.route}")
            route = e.route
            page.views.clear()
            if route == "/dashboard":
                view = Dashboard(store, page)
            elif route == "/create":
                view = CapsuleEditor(store, page, on_save=lambda: page.go("/dashboard"))
            elif route.startswith("/view/"):
                capsule_id = route.split("/view/")[1]
                view = CapsuleViewer(store, page, capsule_id)
            else:
                logging.warning(f"Unknown route: {route}. Redirecting to dashboard.")
                view = Dashboard(store, page)
            page.views.append(layout.get_layout(view.build()))
            logging.debug("Viewがページに追加されました。")
            page.update()
        except Exception as ex:
            logging.error(f"Error in route_change: {ex}")
    
    page.on_route_change = route_change
    page.go("/dashboard")

ft.app(target=main) 