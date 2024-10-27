from pathlib import Path
from typing import Optional, Dict, List, Union
from dataclasses import dataclass
import asyncio
import hashlib
from watchfiles import awatch
from concurrent.futures import ThreadPoolExecutor
from fasthtml.common import *

__all__ = [
    "BundleConfig",
    "AssetManager",
    "BundlerMiddleware",
    "FastHTMLBundler",
    "bundled_script",
    "bundled_style",
]


@dataclass
class BundleConfig:
    entry_dir: Path
    output_dir: Path
    watch: bool = False
    minify: bool = True
    sourcemaps: bool = True
    cache_dir: Path = Path(".bundle_cache")
    dev_mode: bool = False


class AssetManager:
    def __init__(self, config: BundleConfig):
        self.config = config
        self.asset_map: Dict[str, str] = {}  # Original path -> Bundled path
        self.hash_map: Dict[str, str] = {}  # File content hash -> Bundled path
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def init(self):
        """Initialize asset processing"""
        self.config.output_dir.mkdir(exist_ok=True)
        self.config.cache_dir.mkdir(exist_ok=True)

        if self.config.watch:
            asyncio.create_task(self._watch_assets())

    async def _watch_assets(self):
        """Watch for file changes and rebuild assets"""
        async for changes in awatch(self.config.entry_dir):
            await self.rebuild_changed(changes)

    async def rebuild_changed(self, changes):
        """Rebuild changed assets"""
        for change in changes:
            await self.process_asset(Path(change[1]))

    async def process_asset(self, path: Path) -> str:
        """Process a single asset file"""
        if path.suffix == ".css":
            return await self._process_css(path)
        elif path.suffix == ".js":
            return await self._process_js(path)
        return str(path)

    async def _process_js(self, path: Path) -> str:
        """Process JavaScript files"""
        processor = JavaScriptProcessor()
        content = path.read_text()

        # Check cache first
        file_hash = hashlib.md5(content.encode()).hexdigest()
        if cached := self.cache.get(file_hash):
            return cached

        processed = await processor.process(
            content,
            {"minify": self.config.minify, "sourcemaps": self.config.sourcemaps},
        )

        output_path = self._get_output_path(path, file_hash)
        output_path.write_text(processed)

        self.asset_map[str(path)] = str(output_path)
        self.hash_map[file_hash] = str(output_path)

        return str(output_path)

    async def _process_css(self, path: Path) -> str:
        """Process CSS files"""
        processor = CSSProcessor()
        content = path.read_text()

        file_hash = hashlib.md5(content.encode()).hexdigest()
        if cached := self.cache.get(file_hash):
            return cached

        processed = await processor.process(
            content,
            {
                "minify": self.config.minify,
                "file_type": path.suffix,
                "sourcemaps": self.config.sourcemaps,
            },
        )

        output_path = self._get_output_path(path, file_hash)
        output_path.write_text(processed)

        self.asset_map[str(path)] = str(output_path)
        self.hash_map[file_hash] = str(output_path)

        return str(output_path)

    def _get_output_path(self, original_path: Path, file_hash: str) -> Path:
        """Generate output path with hash for cache busting"""
        stem = original_path.stem
        suffix = original_path.suffix
        return self.config.output_dir / f"{stem}.{file_hash[:8]}{suffix}"


class BundlerMiddleware:
    """Middleware to handle asset serving and processing"""

    def __init__(self, config: BundleConfig):
        self.asset_manager = AssetManager(config)

    async def __call__(self, scope, receive, send):
        await self.asset_manager.init()
        # Handle asset requests...


# Main bundler integration
class FastHTMLBundler:
    def __init__(self, app, config: BundleConfig):
        self.app = app
        self.config = config
        self.asset_manager = AssetManager(config)

    async def setup(self):
        # Setup bundler and initialize asset processing
        await self.asset_manager.init()
        self.app.middleware("http")(BundlerMiddleware(self.config))

    def asset(self, path: str) -> str:
        # Get bundled asset path
        return self.asset_manager.asset_map.get(path, path)


def bundled_script(src: str, **kwargs) -> FT:
    # Create a script tag with bundled source
    return Script(src=bundler.asset(src), **kwargs)


def bundled_style(href: str, **kwargs) -> FT:
    # Create a link tag with bundled stylesheet
    return Link(rel="stylesheet", href=bundler.asset(href))
