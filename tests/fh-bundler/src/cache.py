from typing import Any

import pickle
from pathlib import Path


class BundleCache:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)

    def get(self, key: str) -> Any:
        cache_file = self.cache_dir / f"{key}.cache"
        if cache_file.exists():
            with cache_file.open("rb") as f:
                return pickle.load(f)
        return None

    def set(self, key: str, value: Any):
        cache_file = self.cache_dir / f"{key}.cache"
        with cache_file.open("wb") as f:
            pickle.dump(value, f)
