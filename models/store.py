from dataclasses import dataclass
from datetime import datetime
import uuid
import json
from pathlib import Path
from typing import Dict, List, Optional
import logging
from models.capsule import CapsuleData

class CapsuleStore:
    def __init__(self):
        self.capsules: Dict[str, CapsuleData] = {}
        self.load_data()

    def add_capsule(self, capsule: CapsuleData) -> bool:
        logging.debug(f"キャプセルを追加します: {capsule.id}")
        if not self.is_valid_code(capsule.code):
            logging.error(f"無効なコードが含まれています: {capsule.id}")
            return False  # 無効なコードの場合は追加しません
        self.capsules[capsule.id] = capsule
        self.save_data()
        return True

    def get_capsule(self, capsule_id: str) -> Optional[CapsuleData]:
        return self.capsules.get(capsule_id)

    def get_all_capsules(self) -> List[CapsuleData]:
        logging.debug(f"全キャプセル数: {len(self.capsules)}")
        return list(self.capsules.values())

    def load_data(self):
        data_file = Path(__file__).parent.parent / "capsules.json"
        logging.debug(f"キャプセルデータをロードします: {data_file.resolve()}")
        if data_file.exists():
            try:
                data = json.loads(data_file.read_text())
                self.capsules = {
                    k: CapsuleData.from_dict(v) for k, v in data.items()
                }
                logging.debug(f"ロードされたキャプセル数: {len(self.capsules)}")
            except Exception as e:
                logging.error(f"データ読み込み時にエラー: {e}")
                self.capsules = {}
        else:
            self.capsules = {}

    def save_data(self):
        data = {k: v.to_dict() for k, v in self.capsules.items()}
        try:
            data_file = Path(__file__).parent.parent / "capsules.json"
            logging.debug(f"キャプセルデータを保存します: {data_file.resolve()}")
            data_file.write_text(json.dumps(data, ensure_ascii=False, indent=4))
            logging.debug("キャプセルデータが正常に保存されました。")
        except Exception as e:
            logging.error(f"データ保存時にエラー: {e}") 

    def is_valid_code(self, code: str) -> bool:
        try:
            # コードがUTF-8でエンコード可能かチェック
            code.encode('utf-8')
            return True
        except UnicodeEncodeError:
            return False 