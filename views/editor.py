import logging
import flet as ft
from datetime import datetime
from models.capsule import CapsuleData
from models.store import CapsuleStore

class CapsuleEditor(ft.View):
    def __init__(self, store: CapsuleStore, page: ft.Page, on_save=None):
        super().__init__(route="/create")
        self.store = store
        self.page = page
        self.on_save = on_save

    def build(self):
        logging.info("CapsuleEditor ビューの build メソッドが呼び出されました。")
        try:
            self.code_editor = ft.TextField(
                multiline=True,
                min_lines=10,
                max_lines=20,
                label="コード",
                text_style=ft.TextStyle(
                    font_family="RobotoMono",
                    color="white",
                    size=14
                ),
                bgcolor="#1E1E1E",
                border_color="#323232"
            )
            
            self.message_editor = ft.TextField(
                multiline=True,
                min_lines=3,
                max_lines=5,
                label="メッセージ",
                border_color="#323232"
            )

            content = ft.Column([
                ft.Text("新しいタイムカプセル", size=24, weight=ft.FontWeight.BOLD),
                self.code_editor,
                self.message_editor,
                ft.ElevatedButton(
                    "タイムカプセルを埋める",
                    on_click=self.save_capsule
                )
            ], spacing=20)
            
            return content
        except Exception as e:
            logging.error(f"CapesuleEditor.build でエラーが発生しました: {e}")
            return ft.Text("エラーが発生しました。")

    def save_capsule(self, e):
        logging.info("save_capsule メソッドが呼び出されました。")
        try:
            if not self.code_editor.value or not self.message_editor.value:
                logging.warning("コードまたはメッセージが入力されていません。")
                self.page.snack_bar = ft.SnackBar(ft.Text("コードとメッセージを入力してください"))
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            capsule = CapsuleData.create(
                code=self.code_editor.value,
                message=self.message_editor.value,
                open_at=datetime.now()  # MVPでは現在時刻を使用
            )
            
            success = self.store.add_capsule(capsule)
            if not success:
                logging.warning(f"無効なコードが含まれています: {capsule.id}")
                self.page.snack_bar = ft.SnackBar(ft.Text("無効なコードが含まれています。"))
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            logging.info(f"キャプセルが正常に追加されました: {capsule.id}")
            if self.on_save:
                self.on_save()
        except Exception as e:
            logging.error(f"save_capsule でエラーが発生しました: {e}")
            self.page.snack_bar = ft.SnackBar(ft.Text("キャプセルの保存中にエラーが発生しました。"))
            self.page.snack_bar.open = True
            self.page.update()

    def on_page_load(self, e):
        logging.info("on_page_load メソッドが呼び出されました。")
        self.update() 