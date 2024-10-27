import datetime
from pathlib import Path
from typing import Dict
import json


def create_manifest(asset_map: Dict[str, str], output_dir: Path):
    """Create asset manifest file"""
    manifest = {"assets": asset_map, "generated": datetime.now().isoformat()}
    manifest_path = output_dir / "asset-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
