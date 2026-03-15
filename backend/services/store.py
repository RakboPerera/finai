"""JSON file store for application state (replaces PostgreSQL)."""
import json
from pathlib import Path
from datetime import datetime
from config import STORE_DIR


class JSONStore:
    def __init__(self):
        self.store_dir = STORE_DIR

    def _get_path(self, collection: str) -> Path:
        path = self.store_dir / f"{collection}.json"
        if not path.exists():
            path.write_text("[]")
        return path

    def read(self, collection: str) -> list:
        path = self._get_path(collection)
        return json.loads(path.read_text())

    def write(self, collection: str, data: list):
        path = self._get_path(collection)
        path.write_text(json.dumps(data, indent=2, default=str))

    def append(self, collection: str, item: dict):
        data = self.read(collection)
        item["_id"] = len(data) + 1
        item["_created_at"] = datetime.now().isoformat()
        data.append(item)
        self.write(collection, data)
        return item

    def find(self, collection: str, filters: dict = None) -> list:
        data = self.read(collection)
        if not filters:
            return data
        results = []
        for item in data:
            match = all(item.get(k) == v for k, v in filters.items())
            if match:
                results.append(item)
        return results

    def find_one(self, collection: str, filters: dict) -> dict | None:
        results = self.find(collection, filters)
        return results[0] if results else None

    def update(self, collection: str, filters: dict, updates: dict):
        data = self.read(collection)
        updated = 0
        for item in data:
            if all(item.get(k) == v for k, v in filters.items()):
                item.update(updates)
                item["_updated_at"] = datetime.now().isoformat()
                updated += 1
        self.write(collection, data)
        return updated

    def delete(self, collection: str, filters: dict):
        data = self.read(collection)
        original_len = len(data)
        data = [item for item in data if not all(item.get(k) == v for k, v in filters.items())]
        self.write(collection, data)
        return original_len - len(data)


store = JSONStore()
