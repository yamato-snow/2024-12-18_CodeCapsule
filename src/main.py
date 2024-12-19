import flet as ft
from datetime import datetime
import uuid
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional

# モデル定義
@dataclass
class CapsuleData:
    id: str
    code: str
    message: str
    created_at: datetime
    open_at: datetime

    @classmethod
    def create(cls, code: str, message: str, open_at: datetime):
        return cls(
            id=str(uuid.uuid4()),
            code=code,
            message=message,
            created_at=datetime.now(),
            open_at=open_at
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "code": self.code,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
            "open_at": self.open_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CapsuleData':
        return cls(
            id=data["id"],
            code=data["code"],
            message=data["message"],
            created_at=datetime.fromisoformat(data["created_at"]),
            open_at=datetime.fromisoformat(data["open_at"])
        )

# ストア実装
class CapsuleStore:
    def __init__(self):
        self.capsules: Dict[str, CapsuleData] = {}
        self.load_data()

    def add_capsule(self, capsule: CapsuleData):
        self.capsules[capsule.id] = capsule
        self.save_data()

    def get_capsule(self, capsule_id: str) -> Optional[CapsuleData]:
        return self.capsules.get(capsule_id)

    def get_all_capsules(self) -> List[CapsuleData]:
        return list(self.capsules.values())

    def load_data(self):
        path = Path("capsules.json")
        if path.exists():
            try:
                data = json.loads(path.read_text())
                self.capsules = {
                    k: CapsuleData.from_dict(v) for k, v in data.items()
                }
            except Exception:
                self.capsules = {}

    def save_data(self):
        data = {k: v.to_dict() for k, v in self.capsules.items()}
        Path("capsules.json").write_text(json.dumps(data))

# エディタ画面
class CapsuleEditor(ft.View):
    def __init__(self, store: CapsuleStore, on_save=None):
        super().__init__()
        self.store = store
        self.on_save = on_save

    def build(self):
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

        return ft.Column([
            ft.Text("新しいタイムカプセル", size=24, weight=ft.FontWeight.BOLD),
            self.code_editor,
            self.message_editor,
            ft.ElevatedButton(
                "タイムカプセルを埋める",
                on_click=self.save_capsule
            )
        ], spacing=20)

    def save_capsule(self, e):
        if not self.code_editor.value or not self.message_editor.value:
            return
        
        capsule = CapsuleData.create(
            code=self.code_editor.value,
            message=self.message_editor.value,
            open_at=datetime.now()  # MVPでは現在時刻を使用
        )
        
        self.store.add_capsule(capsule)
        if self.on_save:
            self.on_save()

    def on_page_load(self, e):
        self.update()

class Dashboard(ft.View):
    def __init__(self, store: CapsuleStore):
        super().__init__()
        self.store = store

    def build(self):
        self.capsules_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
        )
        return ft.Container(
            padding=20,
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Text(
                            "CodeCapsule",
                            size=40,
                            font_family="RobotoMono",
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.ElevatedButton(
                            "新規作成",
                            on_click=lambda _: self.show_editor()
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=20
                ),
                self.capsules_list
            ], spacing=20)
        )

    def show_editor(self):
        self.page.go("/editor")

    def show_dashboard(self):
        self.page.go("/dashboard")

    def calculate_aging_effect(self, created_at: datetime) -> dict:
        days = (datetime.now() - created_at).days
        if days < 7:
            return {"opacity": 1.0, "bgcolor": "#424242"}
        elif days < 30:
            return {"opacity": 0.9, "bgcolor": "#323232"}
        else:
            return {"opacity": 0.8, "bgcolor": "#212121"}

    def update_list(self):
        self.capsules_list.controls.clear()
        for capsule in self.store.get_all_capsules():
            effects = self.calculate_aging_effect(capsule.created_at)
            self.capsules_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(
                                capsule.message[:50] + "..." if len(capsule.message) > 50 else capsule.message,
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(f"作成日: {capsule.created_at:%Y-%m-%d}"),
                            ft.Text(f"コードの長さ: {len(capsule.code)}文字")
                        ]),
                        padding=20,
                        **effects
                    ),
                )
            )
        self.capsules_list.update()

def main(page: ft.Page):
    page.title = "CodeCapsule"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1000
    page.window.height = 800
    
    store = CapsuleStore()
    dashboard = Dashboard(store)
    editor = CapsuleEditor(store, on_save=lambda: page.go("/dashboard"))

    page.views.append(dashboard)
    page.views.append(editor)

    page.go("/dashboard")

ft.app(target=main)