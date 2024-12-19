import json
from pathlib import Path
from typing import Dict, List
from .capsule import CapsuleData

class CapsuleStore:
    def __init__(self):
        self.capsules: Dict[str, CapsuleData] = {}
        self.load_data()

    def add_capsule(self, capsule: CapsuleData):
        self.capsules[capsule.id] = capsule
        self.save_data()

    def get_capsule(self, capsule_id: str) -> CapsuleData:
        return self.capsules.get(capsule_id)

    def get_all_capsules(self) -> List[CapsuleData]:
        return list(self.capsules.values())

    def load_data(self):
        path = Path("capsules.json")
        if path.exists():
            data = json.loads(path.read_text())
            self.capsules = {
                k: CapsuleData.from_dict(v) for k, v in data.items()
            }

    def save_data(self):
        data = {k: v.to_dict() for k, v in self.capsules.items()}
        Path("capsules.json").write_text(json.dumps(data))