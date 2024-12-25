import logging
import flet as ft
from models.store import CapsuleStore
from utils.aging import calculate_aging_effect
from models.capsule import CapsuleData

class CapsuleViewer(ft.View):
    def __init__(self, store: CapsuleStore, page: ft.Page, capsule_id: str):
        super().__init__(route=f"/view/{capsule_id}")
        self.store = store
        self.page = page
        self.capsule_id = capsule_id

    def build(self):
        logging.info("CapsuleViewer の build メソッドが呼び出されました。")
        # キャプセルデータを取得
        capsule = self.store.get_capsule(self.capsule_id)
        if not capsule:
            logging.warning(f"キャプセルが見つかりません: {self.capsule_id}")
            return ft.Text("キャプセルが見つかりません。", size=20)
        
        # キャプセルの詳細を表示
        return ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            controls=[
                ft.Text(f"メッセージ: {capsule.message}", size=20),
                ft.Text(f"コード: {capsule.code}", size=14),
                ft.Text(f"作成日: {capsule.created_at.strftime('%Y-%m-%d')}", size=14),
                ft.Text(f"開封日: {capsule.open_at.strftime('%Y-%m-%d')}", size=14)
            ]
        )

    def set_capsule_id(self, capsule_id: str):
        logging.info(f"Capsule ID を設定します: {capsule_id}")
        self.capsule_id = capsule_id
        self.update() 