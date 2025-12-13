import json
from pathlib import Path

class SaveSystem:
    def __init__(self, base: Path):
        self.base = base
        self.base.mkdir(parents=True, exist_ok=True)

    def save(self, slot: str, run_state: dict, knowledge_state: dict) -> None:
        payload = {"run": run_state, "knowledge": knowledge_state}
        (self.base / f"{slot}.sav").write_text(json.dumps(payload, indent=2))

    def load(self, slot: str) -> tuple[dict, dict]:
        p = self.base / f"{slot}.sav"
        if not p.exists():
            return {}, {}
        data = json.loads(p.read_text())
        return data.get("run", {}), data.get("knowledge", {})
